import csv

from django.shortcuts import redirect

from tables.models import OrdenRegistro, TipoRegistro


def exportaDB(request):
    # First delete all records
    OrdenRegistro.objects.all().delete()
    
    reader = csv.DictReader(open("orden_registros.csv"))
    for raw in reader:
        tr = TipoRegistro.objects.get(id=raw['Tipo'])
        print(raw)
        p = OrdenRegistro(
            tiporegistro=tr,
            name=raw['Campo'],
            fromm=raw['Long'],
            long=raw['Desde'],
            type=raw['Tipo2'],
            description=raw['Observación'],
        )

        p.save()

    return redirect('tables:home')
