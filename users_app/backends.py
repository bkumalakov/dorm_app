from django.contrib.auth.backends import ModelBackend
from .models import Users
from django.db.models import Q


class UsernameAuthenticationBackend:
    @staticmethod
    def authenticate(request, username=None, password=None):
        try:
            user = Users.objects.get(
             Q(username=username)
            )
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except Users.DoesNotExist:
            return None

    @staticmethod
    def get_user(user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return None


class EmailAuthenticationBackend:
    def authenticate(self, request, email=None, password=None):
        try:
            user = Users.objects.get(
             Q(email=email)
            )
            pwd_valid = user.check_password(password)
            if pwd_valid:
                return user
            return None
        except Users.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Users.objects.get(id=user_id)
        except Users.DoesNotExist:
            return None
