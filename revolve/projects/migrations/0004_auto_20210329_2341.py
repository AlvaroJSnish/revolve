# Generated by Django 3.1.7 on 2021-03-29 23:41

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210329_2340'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectconfigfile',
            name='all_columns',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='projectconfigfile',
            name='deleted_columns',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='projectconfigfile',
            name='final_data',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), size=None), blank=True, size=None),
        ),
        migrations.AlterField(
            model_name='projectconfigfile',
            name='saved_columns',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=200), blank=True, size=None),
        ),
    ]
