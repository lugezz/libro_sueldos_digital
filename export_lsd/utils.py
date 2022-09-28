from export_lsd.models import Formato931

NOT_SIJP = [27, 48, 99]
NOT_OS_INSSJP = [27, 99]


def get_value_from_txt(txt_line: str, field_name: str) -> str:
    resp = ''

    qs = Formato931.objects.get(name=field_name)
    if qs:
        resp = txt_line[qs.fromm-1:qs.fromm + qs.long-1]

    return resp


def amount_txt_to_integer(amount_txt: str, mulitp=100) -> int:
    resp = float(amount_txt.replace(',', '.')) * mulitp
    resp = int(resp)

    return resp


def exclude_eventuales(txt_info: str) -> list:
    resp = []
    for legajo in txt_info:
        mod_cont = int(get_value_from_txt(legajo, 'Código de Modalidad de Contratación'))
        if mod_cont != 102:
            resp.append(legajo)
    return resp
