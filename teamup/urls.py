from django.urls import path
from . import views

app_name = "teamup"

urlpatterns = [
    path('', views.home, name='home'),
    path('settings/', views.settings, name='settings'),
]
