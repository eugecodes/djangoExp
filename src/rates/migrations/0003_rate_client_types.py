# Generated by Django 4.2.7 on 2023-11-29 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("rates", "0002_rate_commission"),
    ]

    operations = [
        migrations.AddField(
            model_name="rate",
            name="client_types",
            field=models.JSONField(verbose_name="ClientTypes"),
            preserve_default=False,
        ),
    ]