# Generated by Django 4.1.1 on 2022-09-27 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('orden', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='OrdenRegistros',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('fromm', models.PositiveSmallIntegerField()),
                ('long', models.PositiveSmallIntegerField()),
                ('type', models.CharField(choices=[('AL', 'Alfanumérico'), ('NU', 'Numérico')], default='AL', max_length=2)),
                ('tiporegistro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tables.tiporegistro')),
            ],
        ),
    ]
