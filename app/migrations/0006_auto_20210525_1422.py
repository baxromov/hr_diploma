# Generated by Django 3.1 on 2021-05-25 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_auto_20210525_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='document',
            field=models.FileField(upload_to='documents/', verbose_name='Hujjat(file)'),
        ),
    ]
