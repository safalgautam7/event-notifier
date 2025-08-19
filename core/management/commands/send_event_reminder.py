from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import Event
from django.core.mail import send_mail


class Command(BaseCommand):
    help = "Send reminders for upcoming events"
    
    def handle(self,*args,**options):
        events = Event.objects.filter(reminder_sent = False)
        for event in events:
            if event.needs_reminder:
                send_mail(
                    subject=f"Reminder: {event.name} is coming up!",
                    message=f"Hi {event.user.username}, your event '{event.name}' is scheduled at {event.event_time}.",
                    from_email="no-reply@example.com",
                    recipient_list=[event.user.email],
                )
                event.reminder_sent = True
                event.save()
                self.stdout.write(self.style.SUCCESS(f"Reminder sent for {event.name}"))


