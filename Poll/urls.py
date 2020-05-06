from django.urls import path
from . import views

app_name = "Poll"

urlpatterns = [
    path('poll/', views.home, name='poll'),
]
