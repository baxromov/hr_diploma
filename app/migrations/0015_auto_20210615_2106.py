# Generated by Django 3.1 on 2021-06-15 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20210615_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='parol'),
        ),
        migrations.AddField(
            model_name='staff',
            name='username',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Username'),
        ),
    ]