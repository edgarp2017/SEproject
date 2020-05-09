from django.urls import path
from . import views

app_name = "Voting"

urlpatterns = [
    path('', views.VoteSUFormView, name='vote_SU'),
    path('uservote/', views.uservote, name ='u_vote')
]
