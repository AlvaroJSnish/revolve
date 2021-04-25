# Generated by Django 3.2 on 2021-04-22 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_auto_20210420_2042'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectconfiguration',
            name='training_task_id',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='projectconfiguration',
            name='training_task_status',
            field=models.CharField(choices=[('Pendiente', 'Pendiente'), ('Empezada', 'Empezada'), ('Reintentando', 'Reintentando'), ('Finalizado', 'Finalizado'), ('Rechazado', 'Rechazado'), ('Recibido', 'Recibido'), ('Fallida', 'Fallida')], default='Pendiente', max_length=40),
        ),
    ]