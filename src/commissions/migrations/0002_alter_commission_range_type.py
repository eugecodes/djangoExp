# Generated by Django 4.2.7 on 2023-11-27 17:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commissions', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commission',
            name='range_type',
            field=models.CharField(blank=True, choices=[('power', 'Power'), ('consumption', 'Consumption')], max_length=11, null=True),
        ),
    ]
