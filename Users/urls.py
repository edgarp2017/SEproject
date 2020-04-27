from django.urls import path, include
from .views import (
    NewUserFormView
)
from django.contrib.auth import views

app_name = 'Users'

urlpatterns = [
    path('', NewUserFormView.as_view(), name='new_users')
]
