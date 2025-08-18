from django.urls import path
from .views import EventView

urlpatterns = [
    path('event-occurrence/',EventView.as_view(),name  = 'event-occurrence'),
]