from django.urls import path, include
from .views import auth_via_provider, auth_callback

# клиентское приложение
urlpatterns = [
    path("auth_via_provider/", auth_via_provider, name='auth_via_provider'),
    path("auth_callback/", auth_callback, name='auth_callback'),
]
