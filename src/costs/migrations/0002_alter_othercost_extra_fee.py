# Generated by Django 4.2.7 on 2023-12-04 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='othercost',
            name='extra_fee',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
