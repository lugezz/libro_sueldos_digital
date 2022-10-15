from import_export import resources

from export_lsd.models import Empleado


class EmpleadoResource(resources.ModelResource):
    class Meta:
        model = Empleado
