# Generated by Django 2.0.2 on 2018-02-27 20:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medicos', '0003_auto_20180224_0725'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='especialista',
            options={'permissions': (('list_especialista', 'Can list especialistas'), ('detail_especialista', 'Can detail especialista'))},
        ),
    ]
