# Generated by Django 4.1.1 on 2022-10-25 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0019_alter_liquidacion_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='liquidacion',
            name='nroLiq',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
