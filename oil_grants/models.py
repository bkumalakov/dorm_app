import random
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date
from phonenumber_field.modelfields import PhoneNumberField
Student = get_user_model()


def check_dates(competitions):
    for competition in competitions:
        now = date.today()
        if competition.start <= now:
            competition.status = "goes on"
        if competition.end < now:
            competition.status = "ended"
        competition.save()


class ProgramGroup(models.Model):
    g_name = models.CharField(max_length=150, verbose_name="Наименование направления подготовки")
    g_code = models.CharField(max_length=6, verbose_name="Код направления подготовки")
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.g_code + " - " + self.g_name

    class Meta:
        verbose_name_plural = 'Направления подготовки'
        verbose_name = 'Направление подготовки'


class EdProgram(models.Model):
    DEGREE_TYPES = (
        ('BSc', 'Бакалавриат'),
        ('MSc', 'Магистратура'),
        ('PhD', 'PhD'),
    )

    p_name = models.CharField(max_length=255, verbose_name="Наименование ОП")
    p_code = models.CharField(max_length=8, verbose_name="Код ОП")
    p_degreeLevel = models.CharField(max_length=3, choices=DEGREE_TYPES, verbose_name="Уровень обучения")
    group = models.ForeignKey(ProgramGroup, on_delete=models.CASCADE)
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.p_code + " - " + self.p_name

    class Meta:
        verbose_name_plural = 'Образовательные программы'
        verbose_name = 'Образовательная программа'


class Company(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    contact_num = PhoneNumberField(null=True, blank=True, verbose_name="Контактный номер")
    description = models.TextField(verbose_name="Описание", blank=True)
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Компании недропользователи'
        verbose_name = 'Компания недропользователь'


class UsedCompetitionNumbers(models.Model):
    competition_number = models.CharField(max_length=14)

    def __str__(self):
        return '{}'.format(self.competition_number)

    class Meta:
        verbose_name_plural = "Использованные номера конкурсов"


class Competitions(models.Model):
    CHOICES = (
        ("didn't start", "Не начался"),
        ("goes on", "Продолжается"),
        ("ended", "Завершился"),
    )

    start = models.DateField(verbose_name="Дата начала приема заявок")
    end = models.DateField(verbose_name="Дата начала приема заявок")
    competition_number = models.CharField(max_length=20, blank=True, unique=True)
    description = models.TextField(verbose_name="Описание", blank=True, default="")
    status = models.CharField(choices=CHOICES, max_length=15, default="didn't start", verbose_name="Статус")
    company = models.ForeignKey(Company, related_name="competitions", on_delete=models.CASCADE,
                                verbose_name="Компания недропользователь", blank=True, null=True)
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False, verbose_name="Дата выхода объявления")

    def __str__(self):
        return self.company.name + ", " + self.status

    @staticmethod
    def set_competition_number():
        ids = UsedCompetitionNumbers.objects.all()
        used_ids = []
        for id in ids:
            used_ids.append(id.competition_number)
        while True:
            id = str(random.randint(100000000, 999999999))
            if id not in used_ids:
                UsedCompetitionNumbers.objects.create(competition_number=id)
                return id

    def save(self, *args, **kwargs):
        now = date.today()
        if self.start <= now:
            self.status = "goes on"
        if self.end < now:
            self.status = "ended"
        if not self.id:
            if not self.competition_number:
                self.competition_number = self.set_competition_number()
            else:
                UsedCompetitionNumbers.objects.create(competition_number=self.competition_number)
        super(Competitions, self).save(*args, **kwargs)

    def clean(self):
        if self.end <= self.start:
            raise ValidationError('End date cannot be later than start date')

    class Meta:
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурсы"
        ordering = ["-date_of_add"]


class Applications(models.Model):
    STATUS_TYPES = (
        ('REC', 'Получена'),
        ('REV', 'Рассматривается'),
        ('RET', 'Отправлена на доработку'),
        ('ACC', 'Одобрена'),
        ('REJ', 'Отклонена'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="applications")
    competition = models.ForeignKey('Competitions', on_delete=models.CASCADE, related_name="applications")
    submission_date = models.DateField(verbose_name="Дата подачи заявки", auto_now_add=True)
    essay = models.PositiveIntegerField(verbose_name='Балл за эссе', blank=True, null=True)
    computerTest = models.PositiveIntegerField(verbose_name='Балл компьютерного теста', blank=True, null=True)
    status = models.CharField(max_length=3, choices=STATUS_TYPES, verbose_name="Статус заявки", default="REC")
    description = models.CharField(max_length=1500, verbose_name="Описание", blank=True, default="")
    contract = models.OneToOneField('Contract', on_delete=models.CASCADE, related_name="application", blank=True, null=True)
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def save(self, *args, **kwargs):
        if self.id:
            if self.contract:
                self.contract.company = self.competition.company
                self.contract.student = self.student
                self.contract.save()
        super(Applications, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'Заявки на конкурсы'
        verbose_name = 'Заявка на конкурс'


class Contract(models.Model):
    DURATION_TYPES = (
        ('YR', 'Год'),
        ('SM', 'Семестр')
    )

    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name="Компания спонсор", blank=True, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Обучающийся",  blank=True, null=True)
    sign_date = models.DateField(verbose_name="Дата заключения")
    duration = models.CharField(max_length=3, choices=DURATION_TYPES, verbose_name="Период оплаты учебы")
    fee = models.IntegerField(verbose_name="Сумма гранта")
    contractNo = models.CharField(max_length=15, verbose_name="Номер договора")
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.contractNo

    class Meta:
        verbose_name_plural = 'Списки присвоенных грантов'
        verbose_name = 'Присвоенный грант'
