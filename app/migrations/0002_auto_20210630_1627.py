# Generated by Django 3.1 on 2021-06-30 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='staff',
            name='work_plan',
        ),
        migrations.DeleteModel(
            name='WorkPlan',
        ),
    ]