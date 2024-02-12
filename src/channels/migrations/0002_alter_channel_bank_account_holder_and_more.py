# Generated by Django 4.2.7 on 2023-11-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('channels', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='bank_account_holder',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='bank_account_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='channel',
            name='fiscal_address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
