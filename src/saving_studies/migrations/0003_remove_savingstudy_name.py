# Generated by Django 4.2.7 on 2023-12-05 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('saving_studies', '0002_savingstudy_channel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='savingstudy',
            name='name',
        ),
    ]