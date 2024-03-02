from django.urls import path, include
from .views import ApiEndpoint, secret_page, auth_via_provider, auth_callback

# клиентское приложение
urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("auth_via_provider/", auth_via_provider, name='auth_via_provider'),
    path("auth_callback/", auth_callback, name='auth_callback'),
    path('api/hello', ApiEndpoint.as_view()),
    path('secret', secret_page, name='secret'),
]
