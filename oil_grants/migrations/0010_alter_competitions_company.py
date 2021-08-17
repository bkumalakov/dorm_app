# Generated by Django 3.2.6 on 2021-08-12 09:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('oil_grants', '0009_auto_20210812_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competitions',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='competitions', to='oil_grants.company', verbose_name='Компания недропользователь'),
        ),
    ]
