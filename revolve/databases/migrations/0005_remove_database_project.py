# Generated by Django 3.0.8 on 2021-05-19 20:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0004_database_project'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='database',
            name='project',
        ),
    ]
