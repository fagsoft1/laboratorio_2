# Generated by Django 2.0.2 on 2018-10-01 22:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0019_auto_20181001_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='fecha_ingreso',
            field=models.DateTimeField(default=datetime.datetime(2018, 10, 1, 17, 23, 2, 944019), null=True),
        ),
    ]