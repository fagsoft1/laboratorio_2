# Generated by Django 2.0.2 on 2018-02-24 07:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('examenes', '0005_auto_20180223_0002'),
        ('entidades', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='entidadexamen',
            unique_together={('examen', 'entidad')},
        ),
    ]
