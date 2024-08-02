from django.db import models
from django.contrib.auth.models import User


class OrderStatusChoices(models.TextChoices):
    """
        Статусы заказа
    """
    BASKET = 'OPEN', 'Статус корзины'
    NEW = 'NEW', 'Новый'
    CONFIRMED = 'CONFIRMED', 'Подтвержден'
    ASSEMBLED = 'ASSEMBLED', 'Собран'
    SENT = 'SENT', 'Отправлен'
    DELIVERED = 'DELIVERED', 'Доставлен'
    CANCELED = 'CANCELED', 'Отменен'


class UserTypeChoices(models.TextChoices):
    """
        Типы пользователей
    """
    SHOP = 'SHOP', 'Магазин'
    BUYER = 'BUYER', 'Покупатель'


class Shop(models.Model):
    """
        Модель магазина
    """
    name = models.CharField(max_length=100)
    url = models.URLField()
    owner = models.OneToOneField(User, related_name='shop', on_delete=models.CASCADE)


class Category(models.Model):
    """
        Модель Категории товара
    """
    name = models.CharField(max_length=100)
    shops = models.ManyToManyField(Shop, related_name='categories')


class Product(models.Model):
    """
        Модель товара
    """
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)


class ProductInfo(models.Model):
    """
        Модель информации о продукте
    """
    product = models.ForeignKey(Product, related_name='product_info', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='product_info', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    price_rrc = models.DecimalField(max_digits=10, decimal_places=2)


class Parameter(models.Model):
    """
        Модель параметра
    """
    name = models.CharField(max_length=100)


class ProductParameter(models.Model):
    """
        Модель параметров продукта
    """
    product_info = models.ForeignKey(ProductInfo, related_name='product_parameter', on_delete=models.CASCADE)
    parameter = models.ForeignKey(Parameter, related_name='product_parameter', on_delete=models.CASCADE)
    value = models.CharField(max_length=255)


class Order(models.Model):
    """
        Модель заказа
    """
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    dt = models.DateTimeField(auto_now_add=True)
    status = models.TextField(choices=OrderStatusChoices.choices)


class OrderItem(models.Model):
    """
        Модель элемента заказа
    """
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()


class Contact(models.Model):
    """
        Модель контакта
    """
    user = models.ForeignKey(User, related_name='contacts', on_delete=models.CASCADE)
    type = models.TextField(choices=UserTypeChoices.choices, default=UserTypeChoices.BUYER)
    value = models.CharField(max_length=255)
