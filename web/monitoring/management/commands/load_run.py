from django.core.management import BaseCommand, call_command

from monitoring.models import Email


class Command(BaseCommand):
    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')

        num_objects = Email.objects.all().count()
        if num_objects == 0:
            print("No data available - loading fixture")
            call_command('loaddata', './web/fixture.json')

        call_command('runserver', '0.0.0.0:8000')