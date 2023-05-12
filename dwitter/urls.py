from django.urls import path
from .views import *
app_name = "dwitter"

urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("profile_list/", profile_list, name="profile_list"),
    path("profile/<int:xc>", profile, name="profile"),
    path("login", login_user, name="login"),
    path("logout", logout_user, name="logout"),
    path("password_reset", password_reset_request, name="password_reset")
#     path("password_reset", auth_views.PasswordResetView.as_view(), name="password_reset")
]
