from django.core.management.base import BaseCommand
from events.models import Event
from django.utils import timezone

class Command(BaseCommand):
    help = 'Actualitza els estats dels esdeveniments'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        for e in Event.objects.filter(status='scheduled', scheduled_date__lte=now):
            e.status='live'
            e.save()
        for e in Event.objects.filter(status='live', scheduled_date__lte=now):
            e.status='finished'
            e.save()
        self.stdout.write('Estats actualitzats')
