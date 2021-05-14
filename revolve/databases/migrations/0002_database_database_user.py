# Generated by Django 3.0.8 on 2021-05-12 22:40

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('databases', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='database',
            name='database_user',
            field=django_cryptography.fields.encrypt(models.TextField(default='root')),
        ),
    ]