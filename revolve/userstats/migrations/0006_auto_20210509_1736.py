# Generated by Django 3.0.8 on 2021-05-09 17:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userstats', '0005_auto_20210509_1116'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userstats',
            name='last_week_average_accuracy',
        ),
        migrations.RemoveField(
            model_name='userstats',
            name='last_week_average_error',
        ),
    ]
