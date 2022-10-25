# Generated by Django 4.1.1 on 2022-10-24 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('export_lsd', '0013_alter_empleado_cuil_alter_empresa_cuit'),
    ]

    operations = [
        migrations.CreateModel(
            name='Liquidacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('employees', models.PositiveSmallIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Liquidaciones',
            },
        ),
        migrations.CreateModel(
            name='Presentacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('periodo', models.DateField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.empresa')),
            ],
            options={
                'verbose_name_plural': 'Presentaciones',
            },
        ),
        migrations.DeleteModel(
            name='Registro',
        ),
        migrations.AddField(
            model_name='liquidacion',
            name='presentacion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='export_lsd.presentacion'),
        ),
    ]
