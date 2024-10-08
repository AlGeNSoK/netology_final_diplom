# Generated by Django 5.0.7 on 2024-08-04 22:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_remove_contact_value_contact_apartment_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinfo',
            name='name',
        ),
        migrations.AddField(
            model_name='productinfo',
            name='model',
            field=models.CharField(blank=True, max_length=100, verbose_name='Модель'),
        ),
        migrations.AddField(
            model_name='shop',
            name='state',
            field=models.BooleanField(default=True, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='shops',
            field=models.ManyToManyField(related_name='categories', to='backend.shop', verbose_name='Магазины'),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.TextField(choices=[('OPEN', 'Статус корзины'), ('NEW', 'Новый'), ('CONFIRMED', 'Подтвержден'), ('ASSEMBLED', 'Собран'), ('SENT', 'Отправлен'), ('DELIVERED', 'Доставлен'), ('CANCELED', 'Отменен')], default='OPEN', verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AlterField(
            model_name='parameter',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название параметра'),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to='backend.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='price',
            field=models.PositiveIntegerField(verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='price_rrc',
            field=models.PositiveIntegerField(verbose_name='Рекомендуемая розничная цена'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_info', to='backend.product', verbose_name='Продукт'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_info', to='backend.shop', verbose_name='Магазин'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='parameter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_parameter', to='backend.parameter', verbose_name='Параметр'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='product_info',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_parameter', to='backend.productinfo', verbose_name='Информация о продукте'),
        ),
        migrations.AlterField(
            model_name='productparameter',
            name='value',
            field=models.CharField(max_length=100, verbose_name='Значение'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=100, verbose_name='Название магазина'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shop', to=settings.AUTH_USER_MODEL, verbose_name='Владелец'),
        ),
        migrations.AlterField(
            model_name='shop',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка'),
        ),
    ]
