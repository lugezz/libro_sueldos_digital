# Generated by Django 4.1.1 on 2022-10-15 10:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0012_alter_empleado_cuil_alter_empresa_cuit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleado',
            name='cuil',
            field=models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)]),
        ),
        migrations.AlterField(
            model_name='empresa',
            name='cuit',
            field=models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)]),
        ),
    ]