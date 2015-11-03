from django.core.management.base import BaseCommand

from elvanto_subgroups.models import Link


class Command(BaseCommand):
    help = 'Sync groups'

    def handle(self, *args, **options):
        Link.sync_all()
