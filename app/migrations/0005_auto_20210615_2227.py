# Generated by Django 3.1 on 2021-06-15 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_merge_20210615_2220'),
    ]

    operations = [
        migrations.AlterField(
            model_name='traininganswer',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.staff', verbose_name='Xodim'),
        ),
    ]
