# Generated by Django 4.1.1 on 2022-11-02 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0028_presentacion_employees_txt_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='presentacion',
            name='employees_txt',
        ),
        migrations.RemoveField(
            model_name='presentacion',
            name='remunerativos_txt',
        ),
    ]
