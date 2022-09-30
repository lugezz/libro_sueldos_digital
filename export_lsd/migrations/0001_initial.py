# Generated by Django 4.1.1 on 2022-09-28 09:59

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Razon Social')),
                ('cuit', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)])),
            ],
        ),
        migrations.CreateModel(
            name='TipoRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('order', models.PositiveSmallIntegerField()),
            ],
            options={
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='Registro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employees', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.empresa')),
            ],
        ),
        migrations.CreateModel(
            name='OrdenRegistro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('fromm', models.PositiveSmallIntegerField()),
                ('long', models.PositiveSmallIntegerField()),
                ('type', models.CharField(choices=[('AL', 'Alfabético'), ('AN', 'Alfanumérico'), ('NU', 'Numérico')], default='AN', max_length=2)),
                ('description', models.TextField()),
                ('tiporegistro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.tiporegistro')),
            ],
            options={
                'ordering': ['tiporegistro__order', 'fromm'],
            },
        ),
        migrations.CreateModel(
            name='Formato931',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('fromm', models.PositiveSmallIntegerField()),
                ('long', models.PositiveSmallIntegerField()),
                ('ordenregistro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='export_lsd.ordenregistro')),
            ],
            options={
                'ordering': ['fromm'],
            },
        ),
    ]