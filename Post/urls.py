from django.urls import path
from . import views

app_name = "Post"

urlpatterns = [
    path('delete/<post_id>', views.delete_post, name='delete'),
]
