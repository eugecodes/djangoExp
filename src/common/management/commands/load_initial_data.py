from django.conf import settings
from django.contrib.auth.models import Group
from django.core.management import call_command
from django.core.management.base import BaseCommand

from roles.models import Role


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    # def add_arguments(self, parser):
    #     parser.add_argument("poll_ids", nargs="+", type=int)

    def handle(self, *args, **options):
        call_command("loaddata", "users")
        # raise CommandError('Poll "%s" does not exist' % poll_id)
        self.stdout.write(self.style.SUCCESS(f"Loaded initial data"))

    def initial_group_settings(self):
        channel_support_group, created = Group.objects.get_or_create(
            name=settings.DEFAULT_CHANNEL_SUPPORT,
        )
        channel_support_role, created = Role.objects.get_or_create(
            name=settings.DEFAULT_CHANNEL_SUPPORT, group=channel_support_group
        )
        backoffice_group, created = Group.objects.get_or_create(
            name=settings.DEFAULT_BACKOFFICE,
        )
        backoffice_role, created = Role.objects.get_or_create(
            name=settings.DEFAULT_BACKOFFICE, group=backoffice_group
        )
