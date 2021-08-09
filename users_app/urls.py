from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("main/", Main.as_view(), name="main_url"),
    path("registration/", Registration.as_view(), name="registration_user_url"),
    path("login/", Login.as_view(), name="log_user_url"),
    path("logout/", Logout.as_view(), name="logout_url"),
    path("recovery/", AccountRecovery.as_view(), name="recovery_url"),
    path("activate/<uidb64>/<token>/", VerificationView.as_view(), name='activate_url'),
    path("restore/<uidb64>/<token>/", PasswordRestore.as_view(), name="restore_url"),

]

