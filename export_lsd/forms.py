from django.forms import Field, ModelForm, TextInput, ValidationError

from export_lsd.models import BasicExportConfig, Empresa, Empleado
from export_lsd.tools.import_empleados import is_positive_number


class CuitCuilField(Field):
    def validate(self, value):
        """Check if value consists 11 numeric positive values"""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        if not is_positive_number(str(value)) or len(str(value)) != 11:
            raise ValidationError("Ingrese un valor numerico de 11 dígitos")


class EmpresaForm(ModelForm):
    cuit = CuitCuilField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empresa
        fields = '__all__'
        exclude = ['user']

        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': "Ingrese el nombre de empresa"
                }
            ),
            'cuit': TextInput
            (
                attrs={
                    'placeholder': "Ingrese el número de CUIT",
                    'maxlength': 15,
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class EmpleadoForm(ModelForm):
    cuil = CuitCuilField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['empleado.name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'empleado.name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del empleado',
                }
            ),
            'empleado.cuil': TextInput(
                attrs={
                    'placeholder': "Ingrese el número de CUIL"
                }
            )
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class ConfigEBForm(ModelForm):
    class Meta:
        model = BasicExportConfig
        fields = '__all__'
        exclude = ['user']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
