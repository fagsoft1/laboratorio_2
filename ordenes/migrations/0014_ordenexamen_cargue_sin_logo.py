# Generated by Django 2.0.2 on 2018-07-28 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0013_auto_20180728_0933'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordenexamen',
            name='cargue_sin_logo',
            field=models.BooleanField(default=False),
        ),
    ]