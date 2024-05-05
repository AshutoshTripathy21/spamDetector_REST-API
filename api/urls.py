from django.urls import path
from .views import UserRegistration, UserProfile, SpamMarking, SearchView, UserLogin, login_view
from . import views

urlpatterns = [
    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('profile/<str:phone_number>/', UserProfile.as_view(), name='profile'),
    path('mark-spam/', SpamMarking.as_view(), name='mark-spam'),
    path('search/', SearchView.as_view(), name='search'),
    path('', views.index, name='index'),
    path('login/', login_view, name='login'),
]
