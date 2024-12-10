# Generated by Django 5.1.1 on 2024-12-09 19:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100, verbose_name='Titulo del evento')),
                ('descr', models.CharField(max_length=200, verbose_name='Descripcion del evento')),
                ('requisitos', models.CharField(default='Sin requisitos', max_length=400, verbose_name='Requisitos para el evento')),
                ('cuando', models.DateField(verbose_name='Fecha del evento')),
                ('solidarios', models.IntegerField(default=0, verbose_name='Creditos solidarios')),
                ('culturales', models.IntegerField(default=0, verbose_name='Creditos culturales')),
                ('deportivos', models.IntegerField(default=0, verbose_name='Creditos deportivos')),
                ('fechaCreacion', models.DateTimeField(verbose_name='Fecha y hora de creacion')),
                ('imagen', models.ImageField(default='imagenes_eventos/imagen_default_evento.webp', upload_to='imagenes_eventos/')),
                ('horaInicio', models.TimeField(max_length=10, verbose_name='Hora de inicio')),
                ('horaFin', models.TimeField(max_length=10, verbose_name='Hora de finalizacion')),
                ('Usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='usuarios.usuario')),
            ],
        ),
    ]
