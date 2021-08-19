from django.contrib import admin
from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings
from .decorators import check_recaptcha

urlpatterns = [
    path("registration/", check_recaptcha(Registration.as_view()), name="registration_user_url"),
    path("user/", UserInfoView.as_view(), name="user_info_url"),
    path("user/update/", UpdateUserView.as_view(), name="update_user_url"),
    path("login/", Login.as_view(), name="log_user_url"),
    path("logout/", Logout.as_view(), name="logout_url"),
    path("recovery/", AccountRecovery.as_view(), name="recovery_url"),
    path("password-update/", check_recaptcha(PasswordUpdateView.as_view()), name="password_update"),
    path("activate/<uidb64>/<token>/", VerificationView.as_view(), name='activate_url'),
    path("restore/<uidb64>/<token>/", check_recaptcha(PasswordRestore.as_view()), name="restore_url"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)