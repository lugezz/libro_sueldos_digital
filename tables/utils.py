from tables.models import Formato931


def get_value_from_txt(txt_line: str, field_name: str) -> str:
    resp = ''

    qs = Formato931.objects.get(name=field_name)
    if qs:
        resp = txt_line[qs.fromm-1:qs.fromm + qs.long-1]

    return resp
