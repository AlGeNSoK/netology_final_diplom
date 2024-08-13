from django.contrib.auth import authenticate, login, logout
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from rest_framework.response import Response
import yaml
from backend.models import Product, Shop, Category, Order, Contact, OrderItem, ProductInfo, Parameter, ProductParameter
from backend.serializers import ShopSerializer, CategorySerializer, OrderSerializer, \
    ProductInfoSerializer, ParameterSerializer


class UserRegistrationView(APIView):
    """
        Регистрация нового пользователя
    """

    def post(self, request):
        user = User.objects.create(**request.data)
        user.set_password(request.data.get('password'))
        user.save()
        return Response({'id': user.id})


class LoginView(APIView):
    """
        Аутентификация пользователя
    """

    def post(self, request):
        user = authenticate(**request.data)
        if user and user.is_active:
            login(request, user)
            return Response({'status': 'Аутентификация пройдена', 'Пользователь': user.username})
        else:
            return Response({'status': 'Аутентификация не пройдена'})


class LogoutView(APIView):
    """
        Выход пользователя
    """

    def post(self, request):
        logout(request)
        return Response({'status': 'Выход выполнен'})


class ContactView(APIView):
    """
        Заполнение контактной информации
    """

    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'status': 'Аутентификация не пройдена'})
        contact = Contact.objects.create(user=request.user, **request.data)
        contact.save()
        return Response({'status': 'Контактная информация заполнена'})


class ShopViewSet(ModelViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['name']


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['name', 'shops']


class ProductViewSet(ModelViewSet):
    serializer_class = ProductInfoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = ProductInfo.objects.all().select_related('product', 'shop')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['product', 'model', 'product_parameters', 'shop']
    search_fields = ['product', 'model', 'product_parameters', 'shop', 'quantity', 'price', 'price_rrc']


class ParameterViewSet(ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class OrderViewSet(ModelViewSet):
    """
        Создание, просмотр и удаление заказов
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status']

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


# class NewOrderView(APIView):
#     """
#         Создание нового заказа
#     """
#
#     permission_classes = [IsAuthenticated]
#     def post(self, request):
#         order = Order.objects.create(user=request.user, status=Order.OrderStatusChoices.BASKET)
#         order.save()
#         return Response({'status': 'Заказ создан'})


class BasketView(APIView):
    """
        Редактирование (добавление и удаление товаров) заказа на стадии корзина
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
            Добавление товара в корзину
        """
        order = Order.objects.get(id=request.data.get('order')).id
        if order:
            if order.user == request.user.id:
                if order.status == Order.OrderStatusChoices.BASKET:
                    product = Product.objects.get(id=request.data.get('product')).id
                    quantity = request.data.get('quantity')
                    shop = ProductInfo.objects.get(id=product).shop
                    order_item = OrderItem.objects.create(order=order, product=product, shop=shop, quantity=quantity)
                    order_item.save()
                    return Response({'status': 'Товар добавлен в корзину'})
                else:
                    return Response({'status': False, 'message': 'Заказ уже был оформлен'})
            else:
                return Response({'status': False, 'message': 'Заказ принадлежит другому пользователю'})
        else:
            return Response({'status': False, 'message': 'В запросе не указан заказ'})

    def get(self, request):
        """
            Просмотр содержимого корзины
        """
        order = Order.objects.get(id=request.data.get('order')).id
        if order.user == request.user:
            order_item = OrderItem.objects.filter(order__user=request.user,
                                                  order__status=Order.OrderStatusChoices.BASKET)
            order_item_list = []
            for element in order_item:
                new_element = {'id': element.id, 'product': element.product,
                               'shop': element.shop, 'price': element.product.price,
                               'quantity': element.quantity, 'sum': element.product.price * element.quantity}
                order_item_list.append(new_element)
            order_product = {'Order': order, 'Product_list': order_item_list}
            return Response(order_product)
        else:
            return Response({'status': False, 'message': 'Заказ принадлежит другому пользователю'})

    def patch(self, request):
        """
            Изменение количества товара в корзине
        """
        if request.data.get('quantity'):
            order = Order.objects.get(id=request.data.get('order')).id
            if order.user == request.user:
                order_item = OrderItem.objects.get(id=request.data.get('order_item'),
                                                   order__id=order,
                                                   order__status=Order.OrderStatusChoices.BASKET)
                order_item.quantity = request.data.get('quantity')
                order_item.update()
                return Response({'status': 'Товар удален из корзины'})
            else:
                return Response({'status': False, 'message': 'Заказ принадлежит другому пользователю'})
        else:
            return Response({'status': False, 'message': 'Не указано количество'})

    def delete(self, request):
        """
            Удаление товара из корзины
        """
        order = Order.objects.get(id=request.data.get('order')).id
        if order.user == request.user:
            order_item = OrderItem.objects.get(id=request.data.get('order_item'),
                                               order__id=order,
                                               order__status=Order.OrderStatusChoices.BASKET)
            order_item.delete()
            return Response({'status': 'Товар удален из корзины'})
        else:
            return Response({'status': False, 'message': 'Заказ принадлежит другому пользователю'})


class SupplierUpdate(APIView):
    """Загрузка информации о магазине, категориях товаров, товарах, характеристиках."""
    permission_classes = [IsAuthenticated]

    def post(self, request, file_name):

        if request.user.contact.type != 'SHOP':
            return Response({'status': 'Загрузка доступна только магазину'})

        with open(f'{file_name}', 'r', encoding='UTF-8') as f:
            data = yaml.safe_load(f)
            shop, _ = Shop.objects.get_or_create(name=data['shop'], owner=request.user.contact)
            for category in data['categories']:
                category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                category_object.shops.add(shop.id)
                category_object.save()
            for item in data['goods']:
                product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
                product_info = ProductInfo.objects.create(product_id=product.id,
                                                          shop_id=shop.id,
                                                          model=item['model'],
                                                          quantity=item['quantity'],
                                                          price=item['price'],
                                                          price_rrc=item['price_rrc'])
                for key, value in item['parameters'].items():
                    parameter_object, _ = Parameter.objects.get_or_create(name=key)
                    ProductParameter.objects.create(product_info_id=product_info.id,
                                                    parameter_id=parameter_object.id,
                                                    value=value)
        return Response({'status': 'products added successfully'})
