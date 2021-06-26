# Generated by Django 3.1 on 2021-06-25 11:03

import ckeditor_uploader.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210623_0521'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCulture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.company')),
            ],
            options={
                'verbose_name_plural': 'Company Culture',
                'ordering': ['-created_at'],
            },
        ),
    ]