# Generated by Django 4.1.1 on 2022-11-09 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0031_conceptoliquidacion_tipo_alter_empleado_area'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conceptoliquidacion',
            name='tipo',
            field=models.CharField(default='Rem', max_length=4, verbose_name='Tipo de Concepto'),
        ),
    ]
