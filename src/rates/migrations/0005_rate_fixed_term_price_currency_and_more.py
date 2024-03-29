# Generated by Django 4.2.7 on 2023-11-30 12:44

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0004_rate_energy_price_1_currency_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='fixed_term_price_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='fixed_term_price',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
    ]
