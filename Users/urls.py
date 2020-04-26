from django.urls import path, include
from .views import (
    NewUserFormView
)
from django.contrib.auth import views

app_name = 'Users'

urlpatterns = [
    #path('', LoginView.as_view(), name="Login"),
    path('', NewUserFormView.as_view(), name='new_users')
]