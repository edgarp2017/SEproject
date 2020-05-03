from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import (
    SignUpView,
    LoginView,
    Profile
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Groups.urls', namespace='Groups')),
    path('signup/', SignUpView, name="Signup"), 
    path('login/', LoginView.as_view(), name="Login"), 
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='Logout'),
    path('profile/', Profile, name='Profile'),
    path('user/', include('Users.urls', namespace='Users')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
