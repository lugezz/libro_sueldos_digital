# Generated by Django 4.1.1 on 2022-11-09 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0029_remove_presentacion_employees_txt_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='empleado',
            name='area',
            field=models.CharField(default='Cachula', max_length=120, verbose_name='Área de Trabajo'),
        ),
    ]
