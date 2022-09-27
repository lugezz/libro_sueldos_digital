from datetime import date, datetime

from django.shortcuts import render

from lsd.my_config import lsd_cfg
from tables.utils import get_value_from_txt


def process_reg1(cuit: str, pay_day: date, employees: int):
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
    resp += 'M00001'

    # TODO: Get user
    ds_base = lsd_cfg()['default'].get('dia_base', 30)
    resp += str(ds_base).zfill(2) + str(employees).zfill(6)

    if len(resp) != 35:
        resp = f'Error: Longitud incorrecta ({len(resp)})'

    return resp


def process_reg2(txt_info: str, payday: date):
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
    leg = 1
    for legajo in txt_info:
        cuil = get_value_from_txt(legajo, 'CUIL')
        # TODO: Get user
        area = lsd_cfg()['default'].get('area', '').ljust(50)
        fecha_pago = payday.strftime('%Y%m%d')
        forma_pago = str(lsd_cfg()['default'].get('forma_pago', 0))
        cbu = " " * 22
        fecha_rubrica = " " * 8

        item = f'02{cuil}{str(leg).zfill(10)}{area}{cbu}030{fecha_pago}{fecha_rubrica}{forma_pago}'
        leg += 1

        resp.append(item)

    resp = '\n'.join(resp)

    return resp


def process_reg3(txt_info):
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
    leg = 1
    for legajo in txt_info:
        cuil = get_value_from_txt(legajo, 'CUIL')
        remun = float(get_value_from_txt(legajo, 'Remuneración Imponible 2')) / 100
        no_rem_osysind = float(get_value_from_txt(legajo, 'Remuneración Imponible 9')) / 100 - remun
        no_remun = float(get_value_from_txt(legajo, 'Conceptos no remunerativos')) / 100 - no_rem_osysind
        ds_trab = int(get_value_from_txt(legajo, 'Cantidad de días trabajados'))

        # TODO: Configurar casos como jubilados y directores

        # TODO: Get user
        ccn_sueldo = lsd_cfg()['default'].get('ccn_sueldo', '').ljust(10)
        ccn_no_rem = lsd_cfg()['default'].get('ccn_no_rem', '').ljust(10)
        ccn_no_osysind = lsd_cfg()['default'].get('ccn_no_osysind', '').ljust(10)
        ccn_sijp = lsd_cfg()['default'].get('ccn_sijp', '').ljust(10)
        ccn_inssjp = lsd_cfg()['default'].get('ccn_inssjp', '').ljust(10)
        ccn_os = lsd_cfg()['default'].get('ccn_os', '').ljust(10)
        ccn_sindicato = lsd_cfg()['default'].get('ccn_sindicato', '').ljust(10)
        porc_sindicato = lsd_cfg()['default'].get('porc_sindicato', 0)

        # Sueldo
        item = f'03{cuil} '
        resp.append(item)

        leg += 1

    resp = '\n'.join(resp)

    return resp


def process_reg4(txt_info):
    pass


def process_reg5(txt_info):
    pass


# def export_txt(txt_file, cuit: str, pay_day: date):
def export_txt(request):
    # TODO: Own process
    txt_file = 'tmp/SD_test.txt'
    pay_day = datetime.strptime('2022-08-31', '%Y-%m-%d')
    cuit = '20123456780'

    with open(txt_file) as f:
        txt_info = f.readlines()

    txt_clean_info = [x for x in txt_info if len(x) > 2]
    reg1 = process_reg1(cuit, pay_day, len(txt_clean_info))
    reg2 = process_reg2(txt_clean_info, pay_day)
    reg3 = process_reg3(txt_clean_info, pay_day)

    print(reg1)
    print(reg2)

    return render(request, 'tables/test.html', {'to_print': reg3})
