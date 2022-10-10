from django.core.validators import MinLengthValidator
from django.db import models

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

    def __str__(self) -> str:
        return self.name


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


class Registro(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    employees = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)
