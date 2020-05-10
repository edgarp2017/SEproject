from django.urls import path, include
from django.contrib.auth import views

from .views import NewUserFormView, BlackWhiteBoxesView, WhiteBoxView, BlackBoxView, BlackBoxMessage

app_name = 'Users'

urlpatterns = [
    path('', NewUserFormView.as_view(), name='new_users'),
    path('blackwhite', BlackWhiteBoxesView, name='black_white'),
    path('addbbox', BlackBoxView, name='black_box'),
    path('addwbox', WhiteBoxView, name='white_box'),
    path('message', BlackBoxMessage, name='black_box_message')
]
