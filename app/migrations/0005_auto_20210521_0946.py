# Generated by Django 3.1 on 2021-05-21 09:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210520_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='worlplan',
            name='company',
        ),
        migrations.AddField(
            model_name='staff',
            name='work_plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.worlplan', verbose_name='Ish jadvali'),
        ),
        migrations.AlterField(
            model_name='staff',
            name='gender',
            field=models.CharField(choices=[('male', 'Erkak'), ('female', 'Ayol')], max_length=10, verbose_name='Jinsi'),
        ),
    ]
