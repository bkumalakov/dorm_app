from django.db import models


class ProgramGroup(models.Model):
    g_name = models.CharField(max_length=50, verbose_name="Наиминование направления подготовки")
    g_code = models.CharField(max_length=6, verbose_name="Код направления подготовки")

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

    p_name = models.CharField(max_length=50, verbose_name="Наиминование ОП")
    p_code = models.CharField(max_length=8, verbose_name="Код ОП")
    p_degreeLevel = models.CharField(max_length=3, choices=DEGREE_TYPES, verbose_name="Уровень обучения")
    group = models.ForeignKey(ProgramGroup, on_delete=models.CASCADE)

    def __str__(self):
        return self.p_code + " - " + self.p_name

    class Meta:
        verbose_name_plural = 'Образовательные программы'
        verbose_name = 'Образовательная программа'


class Student(models.Model):
    s_name = models.CharField(max_length=50, verbose_name="Имя")
    s_surname = models.CharField(max_length=50, verbose_name="Фамилия")
    s_fatherName = models.CharField(max_length=50, verbose_name="Отчество", blank=True)
    s_stateID = models.IntegerField(unique=True, verbose_name="ИИН")
    s_email = models.CharField(max_length=50, verbose_name="Email адрес")
    s_phoneNum = models.CharField(max_length=50, verbose_name="Номер телефона")
    edProgram = models.ForeignKey(EdProgram, on_delete=models.CASCADE)
    admission = models.DateField(verbose_name="Дата поступления")
    gpa = models.FloatField(verbose_name="GPA")
    socialStatus = models.CharField(max_length=50, verbose_name="Социальный статус", blank=True)
    placeOfBirht = models.CharField(max_length=50, verbose_name="Место рождения", blank=True)

    def __str__(self):
        return self.s_name + " " + self.s_surname

    class Meta:
        verbose_name_plural = 'Обучающиеся'
        verbose_name = 'Обучающийся'


class Rating(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Обучающийся')
    essay = models.IntegerField(verbose_name='Балл за эссе', blank=True, null=True)
    computerTest = models.IntegerField(verbose_name='Балл компьютерного теста', blank=True, null=True)
    ratingDate = models.DateField(verbose_name='Дата составления рейтинга')

    class Meta:
        verbose_name_plural = 'Рейтинги обучающихся'
        verbose_name = 'Рейтинг обучающихся'


class OilCompany(models.Model):
    name = models.CharField(max_length=50, verbose_name="Наиминование")
    address = models.CharField(max_length=50, verbose_name="Адрес")

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

    class Meta:
        verbose_name_plural = 'Списки присвоенных грантов'
        verbose_name = 'Присвоенный грант'
