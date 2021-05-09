# Generated by Django 3.0.8 on 2021-05-09 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userstats', '0003_auto_20210509_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userstats',
            name='average_accuracy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='average_error',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='last_week_average_accuracy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='userstats',
            name='last_week_average_error',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
