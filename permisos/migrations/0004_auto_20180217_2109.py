# Generated by Django 2.0.2 on 2018-02-17 21:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('permisos', '0003_auto_20180217_1958'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='aditionaldefaultpermission',
            options={'managed': False, 'permissions': (('list_user', 'Can list user'), ('list_permission', 'Can list permission'), ('list_group', 'Can list group'), ('detail_user', 'Can detail user'), ('make_user_superuser', 'Can make user superuser'), ('make_user_staff', 'Can make user staff'), ('make_user_active', 'Can make user active'))},
        ),
    ]