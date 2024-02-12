# Generated by Django 4.2.7 on 2023-11-16 10:49

import channels.choices
from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('bank_account_holder', models.CharField(max_length=255)),
                ('bank_account_number', models.CharField(max_length=255)),
                ('fiscal_address', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=256, unique=True)),
                ('social_name', models.CharField(max_length=256)),
                ('cif', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name': 'Channel',
            },
            bases=(channels.choices.ChannelStatus, models.Model),
        ),
    ]
