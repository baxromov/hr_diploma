# Generated by Django 3.1 on 2022-05-31 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20220531_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staff',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True, verbose_name='Elektron manzil'),
        ),
    ]
