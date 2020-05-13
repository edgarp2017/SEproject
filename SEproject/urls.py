from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import (
    LoginView,
    Profile,
    ApplicationView
)
from Users.views import AppealView
from Poll import views as poll_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Groups.urls', namespace='Groups')),
    path('', include('Voting.urls', namespace='UserVote')),
    path('', include('actions.urls', namespace='actions')),
    path('post/', include('Post.urls', namespace='Post')),
    path('vote/', include('Voting.urls', namespace='Voting')),
    path('apply/', ApplicationView, name="Apply"),
    path('login/', LoginView.as_view(), name="Login"),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='Logout'),
    path('profile/', Profile, name='Profile'),
    path('user/', include('Users.urls', namespace='Users')),
    path('appeal', AppealView, name='appeal'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
