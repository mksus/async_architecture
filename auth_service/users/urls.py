from django.contrib.auth import views as auth_views
from django.urls import include, path
# Create your views here.

# urlpatterns = [
#     path("accounts/login/", auth_views.LoginView.as_view(template_name="users/login.html"), name='login'),
# ]

urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
]