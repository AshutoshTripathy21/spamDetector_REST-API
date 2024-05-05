from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
# Create your views here.
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, Contact, Spam
from .serializers import UserSerializer, ContactSerializer, SpamSerializer, UserLoginSerializer
from django.http import HttpResponse

import logging

logger = logging.getLogger(__name__)

class UserRegistration(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            if User.objects.filter(phone_number=phone_number).exists():
                return Response({'error': 'User with this phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            # Create user
            user = serializer.save()
            logger.info("User registered: %s", user)
            # Create contact for the user
            Contact.objects.create(user=user, name=user.name, phone_number=user.phone_number)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            password = serializer.validated_data.get('password')
            user = authenticate(request, name=name, password=password)
            if user:
                login(request, user)
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
                #print("User logged in:", user)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                #print("Invalid credentials")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs):
        return Response({'detail': 'Use POST method to login'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
class UserProfile(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'phone_number'
    permission_classes = [IsAuthenticated]

class SpamMarking(generics.CreateAPIView):
    queryset = Spam.objects.all()
    serializer_class = SpamSerializer
    permission_classes = [IsAuthenticated]

class SearchView(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return Contact.objects.filter(Q(name__icontains=query) | Q(phone_number=query))
        return Contact.objects.none()

def index(request):
    return HttpResponse('Hello Welcome to REST API')

def login_view(request):
    return render(request, 'login.html')




git branch -M main
git remote add origin https://github.com/AshutoshTripathy21/spamDetector_REST-API.git
git push -u origin main