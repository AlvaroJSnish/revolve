# Generated by Django 3.0.8 on 2021-05-15 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_projectconfigfile_final_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectconfigfile',
            name='file_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
