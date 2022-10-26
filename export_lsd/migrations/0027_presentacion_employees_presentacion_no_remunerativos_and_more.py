# Generated by Django 4.1.1 on 2022-10-26 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0026_liquidacion_employees_liquidacion_no_remunerativos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentacion',
            name='employees',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='presentacion',
            name='no_remunerativos',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='presentacion',
            name='remunerativos',
            field=models.FloatField(default=0.0),
        ),
    ]
