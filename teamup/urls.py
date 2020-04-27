from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='teamup-home'),
    path('setings/', views.settings, name='teamup-settings'),
    path('login', views.login, name='teamup-login'),
    path('signup', views.signup, name='teamup-signup'),
]
