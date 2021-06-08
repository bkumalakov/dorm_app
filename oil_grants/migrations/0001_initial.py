# Generated by Django 3.2.3 on 2021-06-03 09:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EdProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_name', models.CharField(max_length=50, verbose_name='Наиминование ОП')),
                ('p_code', models.CharField(max_length=8, verbose_name='Код ОП')),
                ('p_degreeLevel', models.CharField(choices=[('BSc', 'Бакалавриат'), ('MSc', 'Магистратура'), ('PhD', 'PhD')], max_length=3, verbose_name='Уровень обучения')),
            ],
            options={
                'verbose_name': 'Образовательная программа',
                'verbose_name_plural': 'Образовательные программы',
            },
        ),
        migrations.CreateModel(
            name='OilCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Наиминование')),
                ('address', models.CharField(max_length=50, verbose_name='Адрес')),
            ],
            options={
                'verbose_name': 'Компания недропользователь',
                'verbose_name_plural': 'Компании недропользователи',
            },
        ),
        migrations.CreateModel(
            name='ProgramGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('g_name', models.CharField(max_length=50, verbose_name='Наиминование направления подготовки')),
                ('g_code', models.CharField(max_length=6, verbose_name='Код направления подготовки')),
            ],
            options={
                'verbose_name': 'Направление подготовки',
                'verbose_name_plural': 'Направления подготовки',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_name', models.CharField(max_length=50, verbose_name='Имя')),
                ('s_surname', models.CharField(max_length=50, verbose_name='Фамилия')),
                ('s_fatherName', models.CharField(blank=True, max_length=50, verbose_name='Отчество')),
                ('s_stateID', models.IntegerField(unique=True, verbose_name='ИИН')),
                ('s_email', models.CharField(max_length=50, verbose_name='Email адрес')),
                ('s_phoneNum', models.CharField(max_length=50, verbose_name='Номер телефона')),
                ('admission', models.DateField(verbose_name='Дата поступления')),
                ('gpa', models.FloatField(verbose_name='GPA')),
                ('socialStatus', models.CharField(blank=True, max_length=50, verbose_name='Социальный статус')),
                ('placeOfBirht', models.CharField(blank=True, max_length=50, verbose_name='Место рождения')),
                ('edProgram', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oil_grants.edprogram')),
            ],
            options={
                'verbose_name': 'Обучающийся',
                'verbose_name_plural': 'Обучающиеся',
            },
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('essay', models.IntegerField(blank=True, null=True, verbose_name='Балл за эссе')),
                ('computerTest', models.IntegerField(blank=True, null=True, verbose_name='Балл компьютерного теста')),
                ('ratingDate', models.DateField(verbose_name='Дата составления рейтинга')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oil_grants.student', verbose_name='Обучающийся')),
            ],
            options={
                'verbose_name': 'Рейтинг обучающихся',
                'verbose_name_plural': 'Рейтинги обучающихся',
            },
        ),
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(verbose_name='Дата присвоения')),
                ('duration', models.CharField(choices=[('YR', 'Год'), ('SM', 'Семестр')], max_length=3, verbose_name='Период оплаты')),
                ('fee', models.IntegerField(verbose_name='Сумма гранта')),
                ('contractNo', models.CharField(max_length=15, verbose_name='Номер договора')),
                ('oilCompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oil_grants.oilcompany', verbose_name='Компания недропользователь')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oil_grants.student', verbose_name='Обучающийся')),
            ],
            options={
                'verbose_name': 'Присвоенный грант',
                'verbose_name_plural': 'Списки присвоенных грантов',
            },
        ),
        migrations.AddField(
            model_name='edprogram',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='oil_grants.programgroup'),
        ),
    ]
