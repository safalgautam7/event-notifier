from .serializers import*
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from rest_framework.authtoken.models import Token
from rest_framework import generics,status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login,logout


class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes=[AllowAny]

class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login (request,user)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "username": user.username})
    
    
class LogoutView(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)

