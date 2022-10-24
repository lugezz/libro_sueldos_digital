# TODO: Step by step

"""
1) Export Legajos
2) Export F.931 para datos de nómina y situación revista
3) Cargar Liquidación por liquidación
4) Validación de que la sumatoria de todas las liquidaciones coincida con el txt del F.931
"""


from export_lsd.utils import amount_txt_to_integer, get_value_from_txt


def get_summary_txtF931(txt_file) -> dict:
    result = {
        'Empleados': 0,
        'Eventuales': 0,
        'Remuneración 1': 0,
        'Remuneración 2': 0,
        'Remuneración 4': 0,
        'Remuneración 8': 0,
        'Remuneración 9': 0,
        'Remuneración 10': 0,
        'No Remunerativos': 0,
    }
    with open(txt_file, encoding='latin-1') as f:
        txt_info = f.readlines()

    txt_clean_info = [x for x in txt_info if len(x) > 2]

    for legajo in txt_clean_info:
        mod_cont = int(get_value_from_txt(legajo, 'Código de Modalidad de Contratación'))
        result['Remuneración 1'] += amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 2'))
        result['Remuneración 2'] += amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 2'))
        result['Remuneración 4'] += amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 4'))
        result['Remuneración 8'] += amount_txt_to_integer(get_value_from_txt(legajo, 'Rem.Dec.788/05 - Rem Impon. 8'))
        result['Remuneración 9'] += amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 9'))
        detr = amount_txt_to_integer(get_value_from_txt(legajo, 'Importe a detraer Ley 27430'))
        result['Remuneración 10'] += amount_txt_to_integer(get_value_from_txt(legajo, 'Remuneración Imponible 2')) - detr

        if mod_cont == 102:
            result['Eventuales'] += 1
        else:
            result['Empleados'] += 1

    return result
