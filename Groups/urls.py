from django.urls import path
from . import views

app_name = "Groups"

urlpatterns = [
    path('', views.home, name='home'),
    path('groups/', views.groups, name='groups'),
    path('create/', views.create, name='makegroup'),
    path('groups/<slug:slug>/', views.GroupDetail.as_view(), name='group_detail'),
]
