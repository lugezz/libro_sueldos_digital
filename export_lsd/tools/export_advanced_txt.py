"""
1) Export Legajos
2) Export F.931 para datos de nómina y situación revista
3) Cargar Liquidación por liquidación
4) Validación de que la sumatoria de todas las liquidaciones coincida con el txt del F.931
"""


import datetime
import os
from pathlib import Path

from django.db.models.query import QuerySet
from django.utils.functional import SimpleLazyObject
from pandas import DataFrame

from export_lsd.models import (BulkCreateManager, ConceptoLiquidacion,
                               Empleado, Liquidacion,
                               OrdenRegistro, Presentacion)
from export_lsd.utils import (amount_txt_to_integer, amount_txt_to_float,
                              get_value_from_txt, NOT_SIJP,
                              sync_format)


def get_summary_txtF931(txt_file: Path) -> dict:
    result = {
        'Empleados': 0,
        'Eventuales': 0,
        'Remuneracion_T': 0.0,
        'Remuneración 1': 0.0,
        'Remuneración 2': 0.0,
        'Remuneración 4': 0.0,
        'Remuneración 8': 0.0,
        'Remuneración 9': 0.0,
        'Remuneración 10': 0.0,
        'No Remunerativos': 0.0,
    }
    with open(txt_file, encoding='latin-1') as f:
        txt_info = f.readlines()

    txt_clean_info = [x for x in txt_info if len(x) > 2]

    for legajo in txt_clean_info:
        mod_cont = int(get_value_from_txt(legajo, 'Código de Modalidad de Contratación'))
        result['Remuneracion_T'] += amount_txt_to_float(get_value_from_txt(legajo, 'Remuneración Total'), 1)
        result['Remuneración 1'] += amount_txt_to_float(get_value_from_txt(legajo, 'Remuneración Imponible 2'), 1)
        result['Remuneración 2'] += amount_txt_to_float(get_value_from_txt(legajo, 'Remuneración Imponible 2'), 1)
        result['Remuneración 4'] += amount_txt_to_float(get_value_from_txt(legajo, 'Remuneración Imponible 4'), 1)
        result['Remuneración 8'] += amount_txt_to_float(get_value_from_txt(legajo, 'Rem.Dec.788/05 - Rem Impon. 8'), 1)
        result['Remuneración 9'] += amount_txt_to_float(get_value_from_txt(legajo, 'Remuneración Imponible 9'), 1)
        if mod_cont in NOT_SIJP:
            rem10 = 0
        else:
            detr = amount_txt_to_float(get_value_from_txt(legajo, 'Importe a detraer Ley 27430'), 1)
            rem10 = amount_txt_to_float(get_value_from_txt(legajo, 'Remuneración Imponible 2'), 1) - detr
        result['Remuneración 10'] += rem10
        result['No Remunerativos'] += amount_txt_to_float(get_value_from_txt(legajo, 'Conceptos no remunerativos'), 1)

        if mod_cont == 102:
            result['Eventuales'] += 1
        else:
            result['Empleados'] += 1
    return result


def process_liquidacion(id_presentacion: int, nro_liq: int, payday: datetime, df_liq: DataFrame) -> dict:
    empleados = set(df_liq['Leg'].tolist())

    result = {
        'empleados': len(empleados),
        'remunerativos': 0.0,
        'no_remunerativos': 0.0,
    }

    bulk_mgr = BulkCreateManager()
    presentacion = Presentacion.objects.get(id=id_presentacion)
    payday_str = payday.strftime('%Y-%m-%d')
    empresa = presentacion.empresa
    liquidacion = Liquidacion.objects.create(nroLiq=nro_liq, presentacion=presentacion, payday=payday_str)

    for index, row in df_liq.iterrows():
        empleado = Empleado.objects.get(leg=row["Leg"], empresa=empresa)

        if row['Tipo'] == 'Rem':
            result['remunerativos'] += float(row['Monto'])

        if row['Tipo'] == 'NR':
            result['no_remunerativos'] += float(row['Monto'])

        importe = -row['Monto'] if row['Tipo'] == 'Ap' else row['Monto']

        bulk_mgr.add(ConceptoLiquidacion(liquidacion=liquidacion,
                                         empleado=empleado,
                                         concepto=row['Concepto'],
                                         cantidad=row['Cant'],
                                         importe=importe))
    bulk_mgr.done()

    # Update Liquidación
    liquidacion.employees = result['empleados']
    liquidacion.remunerativos = result['remunerativos']
    liquidacion.no_remunerativos = result['no_remunerativos']
    liquidacion.save()

    # Update Presentación
    presentacion.remunerativos += result['remunerativos']
    presentacion.no_remunerativos += result['no_remunerativos']
    liquidaciones = Liquidacion.objects.filter(presentacion=presentacion).exclude(nroLiq=nro_liq)

    for liq in liquidaciones:
        conc_liqs = ConceptoLiquidacion.objects.filter(liquidacion=liq)
        if conc_liqs:
            for conc_liq in conc_liqs:
                empleados.add(conc_liq.empleado.leg)

    presentacion.employees = len(empleados)
    presentacion.save()

    result['empleados'] = presentacion.employees
    result['remunerativos'] = presentacion.remunerativos
    result['no_remunerativos'] = presentacion.no_remunerativos

    return result


def process_reg1(cuit: str, periodo: datetime.date, employees: int, nro_liq: int) -> str:
    """
    Identificacion del tipo de registro	2	1	2	Alfabético
    CUIT del empleador	11	3	13	Numérico
    Identificación del envío	2	14	15	Alfanumérico
    Período	6	16	21	Numérico
    Tipo de liquidación	1	22	22	Alfanumérico
    Número de liquidación	5	23	27	Numérico
    Dias base	2	28	29	Alfanumérico
    Cantidad de trabajadores informados en registros '04'	6	30	35	Numérico
    """

    resp = f'01{cuit}SJ'
    resp += periodo
    # TODO: Configurar 'M'=mes; 'Q'=quincena; 'S'=semanal
    resp += 'M'
    resp += str(nro_liq).zfill(5)

    # TODO: Configurar
    ds_base = 30
    resp += str(ds_base).zfill(2) + str(employees).zfill(6)

    return resp


def process_reg2(leg_liqs: QuerySet, payday: datetime.date, cuit: str) -> str:
    """
    Identificacion del tipo de registro	2	1	2
    CUIL del trabajador	11	3	13
    Legajo del trabajador	10	14	23
    Dependencia de revista del trabajador	50	24	73
    CBU de acreditación del pago	22	74	95
    Cantidad de días para proporcionar tope	3	96	98
    Fecha de pago	8	99	106
    Fecha de rúbrica	8	107	114
    Forma de pago	1	115	115
    """
    resp = []
    for id_legajo in leg_liqs:
        empleado = Empleado.objects.get(id=id_legajo['empleado'])
        cuil = empleado.cuil
        leg = str(empleado.leg).zfill(10)
        # TODO: Configurar area en empleado
        area = 'Principal'.ljust(50)
        fecha_pago = payday.strftime('%Y%m%d')
        # TODO: Configurar forma de pago. No acreditación porque requiere CBU
        forma_pago = 1
        cbu = " " * 22
        fecha_rubrica = " " * 8

        item = f'02{cuil}{leg}{area}{cbu}030{fecha_pago}{fecha_rubrica}{forma_pago}'

        resp.append(item)

    resp_final = '\r\n'.join(resp)

    return resp_final


def process_reg3(concepto_liq: QuerySet) -> str:
    """
    Identificación del tipo de registro	2	1	2
    CUIL del trabajador	11	3	13
    Código de concepto liquidado por el empleador	10	14	23
    Cantidad	5	24	28
    Unidades	1	29	29
    Importe	15	30	44
    Indicador Débito / Crédito	1	45	45
    Período de ajuste retroactivo	6	46	51
    """
    resp = []

    for concepto in concepto_liq:
        cuil = concepto.empleado.cuil
        cod_con = concepto.concepto.ljust(10)
        cantidad = str(concepto.cantidad*100).zfill(5)
        importe = round(abs(concepto.importe), 2) * 100
        importe = str(int(importe)).zfill(15)
        tipo = 'C' if concepto.importe > 0 else 'D'

        # Genero fila
        item = f'03{cuil}{cod_con}{cantidad}D{importe}{tipo}{" " * 6}'
        resp.append(item)

    resp_final = '\r\n'.join(resp)

    return resp_final


def process_reg4(txt_info: str) -> str:
    resp = []
    reg4_qs = OrdenRegistro.objects.filter(tiporegistro__order=4)

    for legajo in txt_info:
        linea = ''
        mod_cont = int(get_value_from_txt(legajo, 'Código de Modalidad de Contratación'))
        rem2 = amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 2'))
        rem4 = amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 4'))
        rem8 = amount_txt_to_integer(get_value_from_txt(legajo, 'Rem.Dec.788/05 - Rem Impon. 8'))
        rem9 = amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 9'))
        rem10 = amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 2'))
        detr = amount_txt_to_integer(get_value_from_txt(legajo, 'Importe a detraer Ley 27430'))

        for reg in reg4_qs:
            if reg.formatof931:
                # Si está lo vinculo puliendo formato
                tmp_linea = sync_format(get_value_from_txt(legajo, reg.formatof931.name), reg.long, reg.type)
                if (reg.formatof931.name == 'Cónyuge' or
                        reg.formatof931.name == 'Trabajador Convencionado 0-No 1-Si' or
                        reg.formatof931.name == 'Seguro Colectivo de Vida Obligatorio' or
                        reg.formatof931.name == 'Marca de Corresponde Reducción'):

                    tmp_linea = tmp_linea.replace('T', '1').replace('F', '0')

                linea += tmp_linea

            else:
                # Si no está, cargo los casos específicos y dejo vacío el resto (0 números y " " texto)
                if reg.name == 'Identificación del tipo de registro':
                    linea += '04'
                elif reg.name == 'Base imponible 10':
                    rem10 = rem10 - detr

                    if detr == 0 or mod_cont in NOT_SIJP:
                        rem10 = 0

                    linea += str(rem10).zfill(15)
                elif reg.name == 'Base para el cálculo diferencial de aporte de obra social y FSR (1)':

                    # TODO: Ver esta particularidad de LSD
                    # Valido R4
                    # R4 = Rem + NR OS y Sind + Ap.Ad.OS
                    # Ap.Ad.OS = R4 - Rem - NR OS y Sind
                    tipo_nr = '2'
                    resta = rem2 if tipo_nr != '2' else rem9
                    aa_os = rem4 - resta
                    linea += str(aa_os).zfill(15)

                elif reg.name == 'Base para el cálculo diferencial de contribuciones de obra social y FSR (1)':
                    # Valido R8
                    # R8 = Rem + NR OS y Sind + Ct.Ad.OS
                    # Ct.Ad.OS = R8 - Rem - NR OS y Sind
                    tipo_nr = '2'
                    resta = rem2 if tipo_nr != '2' else rem9
                    aa_os = rem8 - resta
                    linea += str(aa_os).zfill(15)

                else:
                    linea += "0" * reg.long

        resp.append(linea)

    resp_final = '\r\n'.join(resp)

    return resp_final


def process_reg4_from_liq(concepto_liq: QuerySet) -> str:
    resp = ''
    # TODO: Generar registro 4 desde liquidación

    return resp


def process_presentacion(presentacion_qs: Presentacion) -> Path:
    # Devuelve el path del archivo comprimido con todas las liquidaciones en txt
    liquidaciones_list = []
    resp = ''

    liquidaciones = Liquidacion.objects.filter(presentacion=presentacion_qs)
    cuit = presentacion_qs.empresa.cuit
    username = presentacion_qs.user.username
    per_liq = presentacion_qs.periodo.strftime('%Y%m')

    fname = f'finaltxt_{username}_{cuit}_{per_liq}'
    fpath = f'static/temp/{fname}'
    f931_txt_path = f'export_lsd/static/temp/{fname}.txt'.replace('finaltxt', 'temptxt')

    with open(f931_txt_path, encoding='latin-1') as f:
        txt_info = f.readlines()

    txt_clean_info = [x for x in txt_info if len(x) > 2]

    for liquidacion in liquidaciones:
        conceptos = ConceptoLiquidacion.objects.filter(liquidacion=liquidacion)
        legajos = conceptos.values('empleado').distinct()
        reg1 = process_reg1(cuit=cuit,
                            periodo=per_liq,
                            employees=liquidacion.employees,
                            nro_liq=liquidacion.nroLiq)
        reg2 = process_reg2(legajos, liquidacion.payday, cuit)
        reg3 = process_reg3(conceptos)
        if liquidaciones.count() == 1:
            reg4 = process_reg4(txt_clean_info)
        else:
            reg4 = process_reg4_from_liq(conceptos)

        # TODO: Eventuales
        reg5 = ''

        final_result = reg1 + '\r\n' + reg2 + '\r\n' + reg3 + '\r\n' + reg4
        if reg5:
            final_result += '\r\n' + reg5

        txt_output_file = f'{fpath}_{liquidacion.nroLiq}.txt'
        txt_sp = txt_output_file.split('/')
        txt_output_file_name = txt_sp[-1]

        if os.path.exists(txt_output_file):
            os.remove(txt_output_file)

        with open(txt_output_file, 'w', encoding='cp1252') as f:
            f.write(final_result)

        liquidaciones_list.append(f'temp/{txt_output_file_name}')

    if len(liquidaciones_list) == 1:
        resp = liquidaciones_list[0]
    else:
        # TODO: Armar un zip de todas las liquidaciones y borrarlas
        pass

    return resp


def get_final_txts(user: SimpleLazyObject, id_presentacion: int) -> Path:
    resp = {
        'path': ''
    }

    # TODO: Configurar eventuales
    presentacion_qs = Presentacion.objects.get(id=id_presentacion)
    cuit = presentacion_qs.empresa.cuit
    username = presentacion_qs.user.username
    per_liq = presentacion_qs.periodo.strftime('%Y%m')

    fname = f'temptxt_{username}_{cuit}_{per_liq}'
    fpath = f'export_lsd/static/temp/{fname}.txt'
    info_txt = get_summary_txtF931(fpath)

    # 1) Valido empleados
    if presentacion_qs.employees != info_txt['Empleados']:
        resp['error'] = f'Empleados en txt: {info_txt["Empleados"]}. '
        resp['error'] += f'Empleados en liquidaciones: {presentacion_qs.employees}. '
        resp['error'] += 'Por favor corrija esta situación'

        return resp

    # 2) Valido remuneración
    if presentacion_qs.remunerativos != info_txt['Remuneración 2']:
        resp['error'] = f'Remuneración en txt: $ {info_txt["Remuneración 2"]:.2f}. '
        resp['error'] += f'Remuneración en liquidaciones: $ {presentacion_qs.remunerativos:.2f}. '
        resp['error'] += 'Por favor corrija esta situación'

        return resp

    # Listo vamos con el procesamiento
    resp['path'] = process_presentacion(presentacion_qs)

    return resp
