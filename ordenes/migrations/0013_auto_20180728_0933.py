# Generated by Django 2.0.2 on 2018-07-28 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0012_orden_codigo_consulta_web'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ordenexamen',
            options={'permissions': [('list_pendientes_ordenexamen', 'Can list orden examen pendientes'), ('list_con_resultados_ordenexamen', 'Can list orden examen con resultados'), ('list_verificados_ordenexamen', 'Can list orden examen verificados'), ('firmar_como_ordenexamen', 'Can firmar como orden examen'), ('verificar_ordenexamen', 'Can verificar orden examen'), ('imprimir_sin_logo_ordenexamen', 'Can print sin logo orden examen')]},
        ),
    ]
