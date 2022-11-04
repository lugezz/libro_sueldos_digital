"""
1) Export Legajos
2) Export F.931 para datos de nómina y situación revista
3) Cargar Liquidación por liquidación
4) Validación de que la sumatoria de todas las liquidaciones coincida con el txt del F.931
"""


import datetime
import os
from pathlib import Path

from django.utils.functional import SimpleLazyObject
from pandas import DataFrame

from export_lsd.models import BulkCreateManager, ConceptoLiquidacion, Empleado, Liquidacion, Presentacion
from export_lsd.utils import amount_txt_to_float, get_value_from_txt, NOT_SIJP


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

        bulk_mgr.add(ConceptoLiquidacion(liquidacion=liquidacion,
                                         empleado=empleado,
                                         concepto=row['Concepto'],
                                         cantidad=row['Cant'],
                                         importe=row['Monto']))
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


def process_reg1(cuit: str, pay_day: datetime.date, employees: int) -> str:
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
    resp += pay_day.strftime('%Y%m')
    # TODO: Configurar 'M'=mes; 'Q'=quincena; 'S'=semanal
    resp += 'M00001'

    # TODO: Configurar
    ds_base = 30
    resp += str(ds_base).zfill(2) + str(employees).zfill(6)

    return resp


def process_reg2(txt_info: str, payday: datetime.date, cuit: str) -> str:
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
    for legajo in txt_info:
        cuil = get_value_from_txt(legajo, 'CUIL')
        leg = Empleado.objects.filter(empresa__cuit=cuit, cuil=cuil).first().leg
        # TODO: Configurar area en empleado
        area = 'Principal'.ljust(50)
        fecha_pago = payday.strftime('%Y%m%d')
        # TODO: Configurar forma de pago. No acreditación porque requiere CBU
        forma_pago = 1
        cbu = " " * 22
        fecha_rubrica = " " * 8

        item = f'02{cuil}{str(leg).zfill(10)}{area}{cbu}030{fecha_pago}{fecha_rubrica}{forma_pago}'

        resp.append(item)

    resp_final = '\r\n'.join(resp)

    return resp_final


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
        reg1 = process_reg1(cuit,
                            liquidacion.payday,
                            liquidacion.employees)
        reg2 = process_reg2(txt_clean_info, liquidacion.payday, cuit)
        # reg3 = process_reg3(txt_no_eventuales, export_config)
        reg3 = ''
        # reg4 = process_reg4(txt_clean_info, export_config)
        reg4 = ''
        # reg5 = process_reg5(txt_just_eventuales, export_config) if txt_just_eventuales else ''

        final_result = reg1 + '\r\n' + reg2 + '\r\n' + reg3 + '\r\n' + reg4
        # if reg5:
        #     final_result += '\r\n' + reg5

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
