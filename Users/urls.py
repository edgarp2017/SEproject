from django.urls import path, include
from .views import (
    LoginView,
    SignUpView,
    NewUserView
)
from django.contrib.auth import views

app_name = 'Users'

urlpatterns = [
    path('', LoginView.as_view(), name="Login"),
    path('signup/', SignUpView, name='Signup'),
    path('newusers/', NewUserView, name='new_users')
]