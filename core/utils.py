from django.core.mail import send_mail
from django.utils import timezone
from .models import Event

def send_event_reminders():
    events = Event.objects.filter(reminder_sent=False)
    sent_count = 0
    for event in events:
        if event.needs_reminder:  # <-- your property
            send_mail(
                subject=f"Reminder: {event.name} is coming up!",
                message=f"Hi {event.user.username}, your event '{event.name}' is scheduled at {event.event_time}.",
                from_email="no-reply@example.com",
                recipient_list=[event.user.email],
            )
            event.reminder_sent = True
            event.save()
            sent_count += 1
    return sent_count
