"""
1) Export Legajos
2) Export F.931 para datos de nómina y situación revista
3) Cargar Liquidación por liquidación
4) Validación de que la sumatoria de todas las liquidaciones coincida con el txt del F.931
"""


import datetime

from pandas import DataFrame
from export_lsd.models import BulkCreateManager, ConceptoLiquidacion, Empleado, Liquidacion, Presentacion
from export_lsd.utils import amount_txt_to_float, get_value_from_txt, NOT_SIJP


def get_summary_txtF931(txt_file) -> dict:
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
