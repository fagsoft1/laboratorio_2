# Generated by Django 2.0.2 on 2018-07-25 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0011_ordenexamen_fecha_verificado'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='codigo_consulta_web',
            field=models.CharField(max_length=8, null=True),
        ),
    ]