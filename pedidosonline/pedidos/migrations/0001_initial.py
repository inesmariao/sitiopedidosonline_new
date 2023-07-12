# Generated by Django 4.2.2 on 2023-06-22 00:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=45, verbose_name='Nombres')),
                ('apellidos', models.CharField(max_length=45, verbose_name='Apellidos')),
                ('email', models.CharField(max_length=45, verbose_name='Email')),
                ('direccion', models.CharField(max_length=45, verbose_name='Dirección')),
                ('celular', models.CharField(max_length=20, verbose_name='Celular')),
                ('dni', models.CharField(max_length=20, verbose_name='DNI')),
                ('usuario', models.OneToOneField(on_delete=django.db.models.deletion.RESTRICT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('numero', models.CharField(max_length=10, verbose_name='Número')),
                ('total', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Total')),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='pedidos.cliente')),
            ],
        ),
    ]