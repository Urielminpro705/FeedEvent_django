# Generated by Django 5.1.1 on 2024-12-07 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eventos', '0005_evento_requisitos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='fechaCreacion',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha y hora de creacion'),
        ),
        migrations.AlterField(
            model_name='evento',
            name='requisitos',
            field=models.CharField(default='Sin requisitos', max_length=400, verbose_name='Requisitos para el evento'),
        ),
    ]