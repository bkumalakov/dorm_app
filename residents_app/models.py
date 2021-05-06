from django.db import models


class Dorm(models.Model):
    d_name = models.CharField(max_length=50, verbose_name="Наиминование")
    capacity = models.IntegerField(verbose_name="Общее количество мест")

    def __str__(self):
        return self.d_name

    class Meta:
        verbose_name_plural = 'Общежития'
        verbose_name = 'Общежитие'


class Room(models.Model):
    ROOM_TYPE = (
        ('SU', 'Обучающийся'),
        ('NS', 'Не обучающийся'),
    )
    r_number = models.IntegerField(verbose_name="Номер")
    r_floor = models.IntegerField(verbose_name="Этаж")
    r_capacity = models.IntegerField(default=2, verbose_name="Мест")
    dorm_id = models.ForeignKey(Dorm, on_delete=models.CASCADE, verbose_name="Общежитие")
    r_type = models.CharField(max_length=2, choices=ROOM_TYPE, verbose_name="Студенческое/Иное")

    def __str__(self):
        return "Комната: " + str(self.r_number)

    class Meta:
        verbose_name_plural = 'Комнаты'
        verbose_name = 'Комната'


class Application(models.Model):
    TENANT_TYPE = (
        ('SU', 'Обучающийся'),
        ('NS', 'Не обучающийся'),
    )

    SEX_TYPE = (
        ('M', 'Муж.'),
        ('F', 'Жен.'),
    )

    t_type = models.CharField(max_length=2, choices=TENANT_TYPE, verbose_name="Обучающийся/Иное")
    t_name = models.CharField(max_length=60, verbose_name="Имя")
    t_surname = models.CharField(max_length=60, verbose_name="Фамилия")
    t_sex = models.CharField(max_length=1, choices=SEX_TYPE, verbose_name="М/Ж")

    def __str__(self):
        return self.t_name + " " + self.t_surname

    class Meta:
        verbose_name_plural = 'Проживающие'
        verbose_name = 'Проживающий'


class Registration(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Комната")
    tenant = models.ForeignKey(Application, on_delete=models.CASCADE, verbose_name="Проживающий")
    r_order_no = models.IntegerField(verbose_name="Приказ о заселении")
    r_date = models.DateField(verbose_name="Дата приказа о заселении")

    def __str__(self):
        return "Приказ о заселении № " + str(self.r_order_no) + " от " + self.r_date.strftime('%d.%m.%Y')

    class Meta:
        verbose_name_plural = 'Заселения'
        verbose_name = 'Заселение'
