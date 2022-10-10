from django.contrib import admin

from export_lsd.models import (Empleado, Empresa, EmpresaEmpleado,
                               Formato931, OrdenRegistro, TipoRegistro)


admin.site.register(Empleado)
admin.site.register(Empresa)
admin.site.register(EmpresaEmpleado)
admin.site.register(Formato931)
admin.site.register(OrdenRegistro)
admin.site.register(TipoRegistro)
