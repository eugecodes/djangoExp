# Generated by Django 4.2.7 on 2023-11-21 07:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0001_initial'),
        ('roles', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='role',
            unique_together={('name', 'channel'), ('channel', 'admin_role')},
        ),
    ]