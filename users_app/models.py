from datetime import timedelta, datetime
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.core.validators import MaxValueValidator, MinValueValidator


def only_int(value):
    if not value.isdigit():
        raise ValidationError('ID contains characters')


class UserManager(BaseUserManager):
    def create_user(self, username, password=None, email=None):
        if not username:
            raise TypeError("Users must have a username")

        user = self.model(
            email=email,
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, password, username,):
        user = self.create_user(
            username=username,
            password=password,

        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)


class Users(AbstractBaseUser):
    CHOICES = (
        ('студент', 'Студент'),
        ('админ', 'Админ'),
    )
    first_name = models.CharField(max_length=100,  verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    patronymic = models.CharField(max_length=100, blank=True, verbose_name="Отчество", null=True)
    username = models.CharField(max_length=100, unique=True,  verbose_name="Логин", null=True)
    uin = models.CharField(max_length=12, unique=True,  verbose_name="ИИН", validators=[only_int, MinLengthValidator(12)], null=True)
    status = models.CharField(max_length=15, choices=CHOICES, default='студент')
    email = models.EmailField(max_length=140, unique=True, verbose_name="Email адрес")
    phone_number = PhoneNumberField(null=True, blank=True, verbose_name="Номер телефона")
    birthplace = models.CharField(max_length=255, blank=True, default="", verbose_name="Место рождения")
    social_status = models.CharField(max_length=255, blank=True, default="", verbose_name="Социальный статус",)
    receipt_date = models.DateField(null=True, )
    edProgram = models.ForeignKey("oil_grants.EdProgram", on_delete=models.CASCADE, related_name="users", null=True,)
    gpa = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(4)], null=True,)
    image = models.ImageField(upload_to='images/users/avatar', blank=True, null=True, verbose_name="Изображение")
    date_joined = models.DateTimeField(verbose_name='date_joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last_login', auto_now=True)
    last_update = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email', ]

    objects = UserManager()

    def save(self, *args, **kwargs):
        if self.is_admin:
            self.status = 'админ'
        super(Users, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    class Meta:
        verbose_name_plural = "Пользователи"
        verbose_name = "Пользователь"
