from django.urls import path,include
from .views import EventView,ReminderTriggerView

urlpatterns = [
    path('event-occurrence/',EventView.as_view(),name  = 'event-occurrence'),
    path('reminders/trigger/', ReminderTriggerView.as_view(), name="reminder-trigger")
]