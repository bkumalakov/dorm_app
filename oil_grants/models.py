from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date

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

    p_name = models.CharField(max_length=150, verbose_name="Наименование ОП")
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


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="rating",  verbose_name='Обучающийся')
    essay = models.IntegerField(verbose_name='Балл за эссе', blank=True, null=True)
    computerTest = models.IntegerField(verbose_name='Балл компьютерного теста', blank=True, null=True)
    ratingDate = models.DateField(verbose_name='Дата составления рейтинга')
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return "Обучающийся: " + ' ' + self.student.first_name + ' ' + self.student.last_name + " (" + self.ratingDate.strftime("%m/%d/%Y") + ")"

    class Meta:
        verbose_name_plural = 'Рейтинги обучающихся'
        verbose_name = 'Рейтинг обучающихся'


class OilCompany(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наименование")
    address = models.CharField(max_length=50, verbose_name="Адрес")
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Компании недропользователи'
        verbose_name = 'Компания недропользователь'


class Grant(models.Model):
    DURATION_TYPES = (
        ('YR', 'Год'),
        ('SM', 'Семестр')
    )

    oilCompany = models.ForeignKey(OilCompany, on_delete=models.CASCADE, verbose_name="Компания недропользователь")
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name="Обучающийся")
    date = models.DateField(verbose_name="Дата присвоения")
    duration = models.CharField(max_length=3, choices=DURATION_TYPES, verbose_name="Период оплаты")
    fee = models.IntegerField(verbose_name="Сумма гранта")
    contractNo = models.CharField(max_length=15, verbose_name="Номер договора")
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.contractNo

    class Meta:
        verbose_name_plural = 'Списки присвоенных грантов'
        verbose_name = 'Присвоенный грант'


class Participants(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="applications",
                                verbose_name="Учащийся")
    is_passed = models.BooleanField(default=False, verbose_name="Прошел конкурс")
    competition = models.ForeignKey('Competitions', on_delete=models.CASCADE, related_name="participants",
                                    verbose_name="Конкурс")
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.student.first_name + " " + self.student.last_name + " " + str(self.is_passed)

    class Meta:
        verbose_name = "Заявка на конкурс"
        verbose_name_plural = "Заявки на конкурсы"


class Competitions(models.Model):
    CHOICES = (
        ("didn't start", "Не начался"),
        ("goes on", "Продолжается"),
        ("ended", "Завершился"),
    )

    start = models.DateField(verbose_name="Дата начала конкурса")
    end = models.DateField(verbose_name="Дата Завершения конкурс")
    status = models.CharField(choices=CHOICES, max_length=15, default="didn't start", verbose_name="Статус")
    company = models.ForeignKey(OilCompany, related_name="competitions", on_delete=models.CASCADE,
                                verbose_name="Компания недропользователь")
    date_of_update = models.DateTimeField(auto_now=True, editable=False)
    date_of_add = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.company.name + ", " + self.status

    def clean(self):
        if self.end <= self.start:
            raise ValidationError('End date cannot be later than start date')

    class Meta:
        verbose_name = "Конкурс"
        verbose_name_plural = "Конкурсы"
