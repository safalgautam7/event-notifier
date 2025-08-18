from django.test import TestCase,SimpleTestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Event
from django.utils import timezone


EVENT_URL = reverse('event-occurrence')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)

class PrivateEventApiTests(TestCase):
    """Test events API with authenticated users."""
    
    def setUp(self):
        self.client = APIClient()
        self.user = create_user(username='testuser',password='testpass123')
        self.client.force_authenticate(self.user)
        
    def test_create_event_sucess(self):
        payload = {
            'event_name':'meeting',
            'event_time':timezone.now().isoformat()
        }
        res = self.client.post(EVENT_URL,payload,format = "json")
        
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Event.objects.count(),1)
        event = Event.objects.first()
        self.assertEqual(event.user,self.user)
        
    def test_user_sees_only_their_events(self):
        other_user = create_user(username='other',password = 'testpass123')
        Event.objects.create(user=other_user, name="Other's Event", event_time=timezone.now())
        Event.objects.create(user=self.user, name="My Event", event_time=timezone.now())
        
        res = self.client.get(EVENT_URL)
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["name"], "My Event")


class PublicEventApiTests(TestCase):
    """Test events API without authentication"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(EVENT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        
