from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from .views import UserRegistrationView, LogoutView

urlpatterns = [
    path('login/', ObtainAuthToken.as_view()),
    path('register/', UserRegistrationView.as_view()),
    path('logout/', LogoutView.as_view()),
]
