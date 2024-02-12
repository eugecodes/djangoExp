# Generated by Django 4.2.7 on 2023-11-29 14:37

import addresses.choices
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('channels', '0002_alter_channel_bank_account_holder_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('address', models.CharField(max_length=256)),
                ('postal_code', models.CharField(max_length=10)),
                ('city', models.CharField(max_length=256)),
                ('province', models.CharField(max_length=256)),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='channels.channel')),
            ],
            options={
                'verbose_name': 'Address',
            },
            bases=(models.Model, addresses.choices.AddressStatus),
        ),
    ]
