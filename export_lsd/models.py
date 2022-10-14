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

FORMAS_PAGO = [
    ('1', 'Efectivo'),
    ('2', 'Cheque'),
    ('3', 'Acreditación'),
]

TIPO_NR = [
    ('0', 'Sólo NR'),
    ('1', 'Base Sindicato'),
    ('2', 'Base Sindicato y Obra Social')
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
    leg = models.PositiveSmallIntegerField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, verbose_name='Nombre', null=True, blank=True)
    cuil = models.CharField(max_length=11, validators=[MinLengthValidator(11)])

    def __str__(self) -> str:
        return f'{self.empresa.name} - Leg.{self.leg}: {self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        item['empresa'] = self.empresa.name
        return item

    class Meta:
        ordering = ['empresa__name', 'leg']
        unique_together = (('leg', 'empresa'),)


class Registro(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    employees = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now_add=True)


class BasicExportConfig(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=120, verbose_name='Nombre')
    dias_base = models.PositiveSmallIntegerField(default=30, verbose_name='Días Base')
    forma_pago = models.CharField(max_length=1, choices=FORMAS_PAGO, default='1', verbose_name='Forma de Pago')
    ccn_sueldo = models.CharField(max_length=20, verbose_name='Concepto Sueldo')
    ccn_no_rem = models.CharField(max_length=20, null=True, blank=True, verbose_name='Concepto NR')
    ccn_no_osysind = models.CharField(max_length=20, null=True, blank=True, verbose_name='Concepto NR OS y Sind')
    ccn_no_sind = models.CharField(max_length=20, null=True, blank=True, verbose_name='Concepto NR Sind.')
    ccn_sijp = models.CharField(max_length=20, verbose_name='Concepto SIJP')
    ccn_inssjp = models.CharField(max_length=20, verbose_name='Concepto INSSJP')
    ccn_os = models.CharField(max_length=20, verbose_name='Concepto OS')
    ccn_sindicato = models.CharField(max_length=20, null=True, blank=True, verbose_name='Concepto Sindicato')
    porc_sindicato = models.FloatField(default=0, verbose_name='Porcentaje Sindicato')
    tipo_nr = models.CharField(max_length=1, choices=TIPO_NR, default='2', verbose_name='Tipo NR')
    area = models.CharField(max_length=120, default='Administración', verbose_name='Área de Trabajo')
    cuit_empleador_eventuales = models.IntegerField(null=True, blank=True, verbose_name='CUIT Empresa Eventual')

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        user = get_current_user()
        if user and not user.pk:
            user = None
        if not self.pk:
            self.user = user
        self.user = user
        return super().save(force_insert, force_update, using, update_fields)

    def __str__(self) -> str:
        return f'{self.user} - {self.name}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        unique_together = (('user', 'name'),)
