# Generated by Django 4.2.7 on 2023-11-30 12:43

from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('rates', '0003_rate_client_types'),
    ]

    operations = [
        migrations.AddField(
            model_name='rate',
            name='energy_price_1_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='energy_price_2_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='energy_price_3_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='energy_price_4_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='energy_price_5_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='energy_price_6_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='power_price_1_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='power_price_2_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='power_price_3_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='power_price_4_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='power_price_5_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AddField(
            model_name='rate',
            name='power_price_6_currency',
            field=djmoney.models.fields.CurrencyField(choices=[('EUR', 'EUR €')], default='EUR', editable=False, max_length=3, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='energy_price_1',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='energy_price_2',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='energy_price_3',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='energy_price_4',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='energy_price_5',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='energy_price_6',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='power_price_1',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='power_price_2',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='power_price_3',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='power_price_4',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='power_price_5',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
        migrations.AlterField(
            model_name='rate',
            name='power_price_6',
            field=djmoney.models.fields.MoneyField(blank=True, decimal_places=6, max_digits=14, null=True),
        ),
    ]
