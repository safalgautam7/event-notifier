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

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name}"
    
