# Generated by Django 2.0.2 on 2018-02-25 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='paciente',
            unique_together={('tipo_documento', 'nro_identificacion')},
        ),
    ]