# Generated by Django 3.1 on 2022-05-31 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20220531_2246'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='date_of_issue',
            field=models.DateField(null=True, verbose_name='Berilgan sana'),
        ),
        migrations.AlterField(
            model_name='document',
            name='note',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='document',
            name='validity_period',
            field=models.DateField(null=True, verbose_name='Amal qilish mudati'),
        ),
    ]
