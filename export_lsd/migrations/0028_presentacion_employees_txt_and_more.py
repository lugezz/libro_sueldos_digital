# Generated by Django 4.1.1 on 2022-11-02 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0027_presentacion_employees_presentacion_no_remunerativos_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='presentacion',
            name='employees_txt',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='presentacion',
            name='remunerativos_txt',
            field=models.FloatField(default=0.0),
        ),
    ]