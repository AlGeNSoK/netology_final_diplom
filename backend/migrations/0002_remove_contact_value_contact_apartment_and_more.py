# Generated by Django 5.0.7 on 2024-08-04 00:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='value',
        ),
        migrations.AddField(
            model_name='contact',
            name='apartment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Квартира'),
        ),
        migrations.AddField(
            model_name='contact',
            name='building',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Строение'),
        ),
        migrations.AddField(
            model_name='contact',
            name='city',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Город'),
        ),
        migrations.AddField(
            model_name='contact',
            name='house',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Дом'),
        ),
        migrations.AddField(
            model_name='contact',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Номер телефона'),
        ),
        migrations.AddField(
            model_name='contact',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Улица'),
        ),
        migrations.AddField(
            model_name='contact',
            name='structure',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Корпус'),
        ),
    ]
