# Generated by Django 3.1 on 2021-06-16 07:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210615_2227'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='training_url',
            field=models.URLField(blank=True, null=True, unique=True),
        ),
    ]