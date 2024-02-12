# Generated by Django 4.2.7 on 2023-11-17 10:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields
import roles.choices


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('channels', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('enabled', 'Enabled'), ('disabled', 'Disabled')], default='enabled', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('name', models.CharField(max_length=256)),
                ('admin_role', models.BooleanField(default=False)),
                ('channel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='channels.channel')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='auth.group')),
            ],
            options={
                'verbose_name': 'Role',
            },
            bases=(models.Model, roles.choices.RoleStatus),
        ),
    ]
