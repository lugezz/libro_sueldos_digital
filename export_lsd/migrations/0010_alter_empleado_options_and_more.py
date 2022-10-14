# Generated by Django 4.1.1 on 2022-10-14 15:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('export_lsd', '0009_remove_empleado_empleado_empleado_cuil_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='empleado',
            options={'ordering': ['empresa__name', 'leg']},
        ),
        migrations.AlterUniqueTogether(
            name='empleado',
            unique_together={('leg', 'empresa')},
        ),
        migrations.CreateModel(
            name='BasicExportConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Nombre')),
                ('dias_base', models.PositiveSmallIntegerField(default=30, verbose_name='Días Base')),
                ('forma_pago', models.CharField(choices=[('1', 'Efectivo'), ('2', 'Cheque'), ('3', 'Acreditación')], default='1', max_length=1, verbose_name='Forma de Pago')),
                ('ccn_sueldo', models.CharField(max_length=20, verbose_name='Concepto Sueldo')),
                ('ccn_no_rem', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto NR')),
                ('ccn_no_osysind', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto NR OS y Sind')),
                ('ccn_no_sind', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto NR Sind.')),
                ('ccn_sijp', models.CharField(max_length=20, verbose_name='Concepto SIJP')),
                ('ccn_inssjp', models.CharField(max_length=20, verbose_name='Concepto INSSJP')),
                ('ccn_os', models.CharField(max_length=20, verbose_name='Concepto OS')),
                ('ccn_sindicato', models.CharField(blank=True, max_length=20, null=True, verbose_name='Concepto Sindicato')),
                ('porc_sindicato', models.FloatField(default=0, verbose_name='Porcentaje Sindicato')),
                ('tipo_nr', models.CharField(choices=[('0', 'Sólo NR'), ('1', 'Base Sindicato'), ('2', 'Base Sindicato y Obra Social')], default='2', max_length=1, verbose_name='Tipo NR')),
                ('area', models.CharField(default='Administración', max_length=120, verbose_name='Área de Trabajo')),
                ('cuit_empleador_eventuales', models.IntegerField(blank=True, null=True, verbose_name='CUIT Empresa Eventual')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
