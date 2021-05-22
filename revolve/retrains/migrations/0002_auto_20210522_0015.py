# Generated by Django 3.0.8 on 2021-05-22 00:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0005_remove_database_project'),
        ('projects', '0012_projectconfiguration_database'),
        ('retrains', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='retrain',
            name='database',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='database_retrain', to='databases.Database'),
        ),
        migrations.AlterField(
            model_name='retrain',
            name='project',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='project_retrain', to='projects.Project'),
        ),
    ]
