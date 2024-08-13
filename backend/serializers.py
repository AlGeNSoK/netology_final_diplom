from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Shop, Category, ProductInfo, Parameter, ProductParameter, Order, OrderItem, Contact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']
        read_only_fields = ['id']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'user', 'type', 'phone', 'city', 'street', 'house', 'structure', 'building', 'apartment']
        read_only_fields = ['id', 'user']


class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'url', 'state']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', ]
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    class Meta:
        model = Product
        fields = ['id', 'name', 'category']
        read_only_fields = ['id']


class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        fields = ['id', 'name']
        read_only_fields = ['id']


class ProductParameterListingFields(serializers.RelatedField):
    def to_representation(self, value):
        return f'{value.parameter}: {value.value}'


class ProductInfoSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shop = ShopSerializer()
    product_parameters = ProductParameterListingFields(queryset=ProductParameter.objects.all(), many=True)

    class Meta:
        model = ProductInfo
        fields = ['product', 'model', 'product_parameters', 'quantity', 'price', 'price_rrc', 'shop']


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'dt', 'status']
        read_only_fields = ['id']


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'shop', 'quantity']
        read_only_fields = ['id']
