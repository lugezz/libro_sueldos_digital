from crum import get_current_user
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator
from django.db import models
from django.forms.models import model_to_dict

DATA_TYPE = [
    ('AL', 'Alfabético'),
    ('AN', 'Alfanumérico'),
    ('NU', 'Numérico'),
]


class TipoRegistro(models.Model):
    name = models.CharField(max_length=120)
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{str(self.order)}: {self.name}'

    class Meta:
        ordering = ['order']


class Formato931(models.Model):
    name = models.CharField(max_length=150)
    fromm = models.PositiveSmallIntegerField()
    long = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{str(self.name)} - From: {self.fromm}'

    class Meta:
        ordering = ['fromm']


class OrdenRegistro(models.Model):
    tiporegistro = models.ForeignKey(TipoRegistro, on_delete=models.CASCADE)
    formatof931 = models.ForeignKey(Formato931, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=120)
    fromm = models.PositiveSmallIntegerField()
    long = models.PositiveSmallIntegerField()
    type = models.CharField(max_length=2, choices=DATA_TYPE, default='AN')
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        has_f931 = '' if not self.formatof931 else ' (Link F931)'

        return f'{str(self.tiporegistro.order)} - From: {self.fromm} - {self.name}{has_f931}'

    class Meta:
        ordering = ['tiporegistro__order', 'fromm']


class Empresa(models.Model):
    name = models.CharField(max_length=120, verbose_name='Razon Social')
    cuit = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        self.user = user
        return super().save(force_insert, force_update, using, update_fields)

    def toJSON(self):
        item = model_to_dict(self)
        return item


class Empleado(models.Model):
    name = models.CharField(max_length=120, verbose_name='Nombre', null=True, blank=True)
    cuil = models.CharField(max_length=11, validators=[MinLengthValidator(11)])

    def __str__(self) -> str:
        return self.name


class EmpresaEmpleado(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    leg = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.empresa} - {self.leg} - {self.empleado}'

    def toJSON(self):
        item = model_to_dict(self)
        item['empresa'] = self.empresa.toJSON()
        item['empleado'] = self.empleado.toJSON()
        return item


class Registro(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    employees = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
