# Generated by Django 3.0.8 on 2021-05-10 14:53

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0007_auto_20210510_1134'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectconfigfile',
            name='final_label',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, default='', max_length=200, null=True), blank=True, null=True, size=None),
        ),
    ]
