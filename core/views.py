from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status 
from .models import Event
from rest_framework.response import Response
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from rest_framework import permissions


class EventView(APIView):
    def post(self,request):
        """Create or get and event for the authenticated user"""
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)
        
        event_name = request.data.get('event_name')
        event_time = request.data.get('event_time')
        
        if not event_time or not event_name:
            print('this error has occurred')
            return Response({ "error":"Required parameters are missing"},status.HTTP_400_BAD_REQUEST)
        
        parsed_time = parse_datetime(event_time)
        print(parsed_time)
        if not parsed_time:
            return Response({'error':'Invalide datetime format'},status=status.HTTP_400_BAD_REQUEST)
        
        event,created= Event.objects.get_or_create(
            user=request.user,
            name = event_name,
            event_time = parsed_time,
        )
        return Response(
            {
                'id':event.id,
                'name':event.name,
                'event_time':str(event.event_time),
                'user':event.user.username,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
        
        
    def get(self,request):
        """Return only the authenticatd user's events."""
        if not request.user.is_authenticated:
            return Response({'error':'Authentication required'},status.HTTP_401_UNAUTHORIZED)
        events = Event.objects.filter(user=request.user).values('id','name','event_time')
        return Response(list(events),status=status.HTTP_200_OK)
        
from .utils import send_event_reminders

class ReminderTriggerView(APIView):
    """Trigger reminder checker manually via an endpoint"""
    permission_classes = [permissions.IsAdminUser]  # Only admin can trigger

    def post(self, request):
        count = send_event_reminders()
        return Response(
            {"message": f"{count} reminder(s) sent."},
            status=status.HTTP_200_OK
        )
                
                