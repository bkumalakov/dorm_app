# Generated by Django 3.2.6 on 2021-08-13 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oil_grants', '0011_alter_edprogram_p_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='address',
            field=models.CharField(max_length=255, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование'),
        ),
    ]
