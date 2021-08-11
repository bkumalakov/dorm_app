import platform
from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
import sys
from django.contrib.auth import login, authenticate, logout
from .models import *
from .forms import *
from .serializers import *
import re
from .permissions import *
from .utils import *
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import *
from django.http import HttpResponse
from django.conf import settings


class AppTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return text_type(user.is_active) + text_type(user.id) + text_type(timestamp)


token_generator = AppTokenGenerator()


'''Functions'''


def get_header(request):
    regex = re.compile('^HTTP_')
    head = dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))
    return head


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def str_to_class(classname):
    return getattr(sys.modules[__name__], classname)


def email_verification(request, user, email):
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = token_generator.make_token(user)
    domain = get_current_site(request).domain
    link = reverse('activate_url', kwargs={'uidb64': uidb64, 'token': token})
    activate_url = 'https://' + domain + link
    send_mail(
        'Confirm your account',
        'Please confirm your account. Use this link to verify your account\n' + activate_url,
        'Atyrau Oil and Gas University',
        [email],
        fail_silently=False,
    )


'''Views'''


class UserInfoView(LoginRequiredMixin, View):
    def get(self, request,):
        return render(self.request, 'users_app/user_info.html',)


class UpdateUserView(LoginRequiredMixin, View):
    def post(self, request):

        form = UpdateUserForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('user_info_url')
        return render(self.request, 'users_app/update_user.html', context={'form': form, })

    def get(self, request,):
        form = UpdateUserForm(instance=request.user)
        return render(self.request, 'users_app/update_user.html', context={'form': form, })


class Main(View):
    @staticmethod
    def get(request):
        users = Users.objects.all()

        return render(request, 'users_app/Main.html', context={'users': users, })


class Logout(View):
    @staticmethod
    def get(request):
        logout(request)
        return redirect('main_url')


class Registration(View):
    def post(self, request):
        bound_form = RegistrationForm(request.POST)
        if bound_form.is_valid():
            bound_form.save()
            obj_cleaned = bound_form.cleaned_data.get('email')
            raw_password = bound_form.cleaned_data.get('password1')
            authenticate(email_or_phone=obj_cleaned, password=raw_password)
            user = Users.objects.get(email__iexact=obj_cleaned)
            user.is_active = False
            user.save()

            return render(request, 'users_app/confirm_account.html')
        return render(request, "users_app/registration.html", context={'form': bound_form, 'errors': bound_form.errors})

    @staticmethod
    def get(request):
        user = request.user
        if user.is_authenticated:
            return redirect('main_url')
        form = RegistrationForm()

        return render(request, "users_app/registration.html", context={'form': form})


class VerificationView(View):
    @staticmethod
    def get(request, uidb64, *args, **kwargs):
        dirty_id = str(urlsafe_base64_decode(uidb64))
        user = get_object_or_404(Users, id=dirty_id[2:len(dirty_id) - 1])
        if user.is_active:
            return render(request, "users_app/Link_not_active.html")
        user.is_active = True
        user.save()
        return redirect('log_user_url')


class Login(View):
    @staticmethod
    def post(request):
        bound_form = LogForm(request.POST)
        verif = ''
        if bound_form.is_valid():
            user = authenticate(username=bound_form.cleaned_data['username'], password=bound_form.cleaned_data['password'], )
            if user.is_verified:
                login(request, user)
                user = Users.objects.get(id=request.user.id)
                user.last_update = datetime.now()
                user.last_login = datetime.now()
                user.save()
                return redirect('main_url')
            else:
                verif = True

            return render(request, 'users_app/Login.html', context={'form_log': bound_form, 'verif': verif})
        return render(request, 'users_app/Login.html', context={'form_log': bound_form, 'verif': verif,
                                                                'errors': bound_form.errors})

    @staticmethod
    def get(request):
        user = request.user
        if user.is_authenticated:
            return redirect('main_url')
        form_log = LogForm()

        return render(request, 'users_app/Login.html', context={'form_log': form_log})


class AccountRecovery(View):
    @staticmethod
    def post(request):
        email = request.POST.get("email")
        email = str(email).strip()

        user = get_object_or_404(Users, email=email)

        if not user.is_verified:
            return render(request, 'users_app/not_verified.html', )

        uidb64 = urlsafe_base64_encode(force_bytes(user.email))
        token = token_generator.make_token(user)
        domain = get_current_site(request).domain
        link = reverse('restore_url', kwargs={'uidb64': uidb64, 'token': token})
        recovery_url = 'http://' + domain + link
        print(recovery_url)
        send_mail(
            'Restore your password',
            'Please click on link to change your password \n' + recovery_url,
            'Атырауский университет нефти и газа',
            [email],
            fail_silently=False,
        )

        return redirect('main_url')

    @staticmethod
    def get(request):
        return render(request, 'users_app/password_recovery.html')


class PasswordRestore(View):
    @staticmethod
    def post(request, uidb64, token):
        email = str(urlsafe_base64_decode(uidb64))[2: len(str(urlsafe_base64_decode(uidb64))) - 1]
        user = Users.objects.get(email=email)
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 == password2:
            try:
                validate_password(password2)
                is_valid = True

            except ValidationError as e:
                return render(request, 'users_app/restore_password.html', context={'email': email,
                                                                                'uidb64': uidb64,
                                                                                'token': token,
                                                                                'errors': e,
                                                                                })

            if is_valid:
                user.set_password(password1)
                user.save()
                return redirect('log_user_url')
        else:
            return render(request, 'users_app/restore_password.html', context={'email': email,
                                                                            'uidb64': uidb64,
                                                                            'token': token,
                                                                            'errors': 'Passwords not equal',
                                                                            })

    @staticmethod
    def get(request, uidb64, token):
        email = str(urlsafe_base64_decode(uidb64))[2: len(str(urlsafe_base64_decode(uidb64)))-1]
        user = Users.objects.get(email=email)
        if not user.is_verified:
            return render(request, 'users_app/not_verified.html',)

        return render(request, 'users_app/restore_password.html', context={'email': email,
                                                                        'uidb64': uidb64,
                                                                        'token': token,
                                                                        })
