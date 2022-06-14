# Generated by Django 3.1 on 2022-05-31 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20220531_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Название должности'),
        ),
        migrations.AlterField(
            model_name='position',
            name='staff_amount',
            field=models.PositiveIntegerField(null=True, verbose_name='Количество штатов'),
        ),
    ]