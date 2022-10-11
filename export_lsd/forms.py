from django.forms import ModelForm, Textarea, TextInput

from export_lsd.models import Empleado, Empresa


class EmpresaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empresa
        fields = '__all__'
        # exclude = ... si necesitara excluir campos

        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': "Ingrese el nombre de empresa"
                }
            ),
            'cuit': Textarea(
                attrs={
                    'placeholder': "Ingrese el número de CUIT"
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['autofocus'] = True

    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'name': TextInput(
                attrs={
                    'placeholder': 'Ingrese el nombre del empleado',
                }
            ),
            'cuil': Textarea(
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
