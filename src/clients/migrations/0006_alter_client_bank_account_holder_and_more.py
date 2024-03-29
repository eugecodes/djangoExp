# Generated by Django 4.2.7 on 2023-11-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_alter_client_channel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='bank_account_holder',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='bank_account_number',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='fiscal_address',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
