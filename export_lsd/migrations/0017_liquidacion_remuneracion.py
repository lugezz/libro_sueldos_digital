# Generated by Django 4.1.1 on 2022-10-24 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0016_presentacion_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='liquidacion',
            name='remuneracion',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
