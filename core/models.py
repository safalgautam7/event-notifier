from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Event(models.Model):
    """Stores the details related to a particular event"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=100)
    event_time = models.DateTimeField()
    created     = models.DateTimeField(editable=False)
    modified    = models.DateTimeField()
    reminder_sent = models.BooleanField(default =False)

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)
    
    @property
    def has_occurred(self):
        return timezone.now() >= self.event_time
    
    @property
    def needs_reminder(self, hours_before=24):
        """Returns True if event is within the next `hours_before` hours and reminder not yet sent"""
        now = timezone.now()
        reminder_time = self.event_time - timezone.timedelta(hours=hours_before)
        return reminder_time <= now < self.event_time and not self.reminder_sent
        
        
        
    
    def __str__(self):
        return f"{self.name}"
    
