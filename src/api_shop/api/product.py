import logging

from django.http import JsonResponse
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

from src.api_shop.models.product import Product
from src.api_shop.models.category import Category
from src.api_shop.models.review import Review
from src.api_shop.models.tag import Tag
from src.api_shop.serializers.category import CategorySerializer
from src.api_shop.serializers.product import ProductShortSerializer, ProductFullSerializer
from src.api_shop.serializers.review import ReviewInSerializer, ReviewOutSerializer
from src.api_shop.serializers.tag import TagSerializer
from src.api_shop.services.comment import CommentsService

logger = logging.getLogger(__name__)


class CategoriesListView(ListModelMixin, GenericAPIView):
    """
    Вывод категорий
    """
    queryset = Category.objects.filter(deleted=False, parent=None)  # Активные родительские категории
    serializer_class = CategorySerializer

    @swagger_auto_schema(tags=['catalog'])
    def get(self, request):
        return self.list(request)


class TagListView(ListModelMixin, GenericAPIView):
    """
    Вывод тегов
    """
    queryset = Tag.objects.filter(deleted=False)  # Только активные теги
    serializer_class = TagSerializer

    @swagger_auto_schema(tags=['tags'])
    def get(self, request):
        return self.list(request)


class ProductDetailView(RetrieveAPIView):
    """
    Вывод данных о товаре (по pk в url)
    """
    queryset = Product.objects.filter(deleted=False)  # Активные товары
    serializer_class = ProductFullSerializer


class ReviewCreateView(CreateModelMixin, GenericAPIView):
    """
    Добавление отзыва к товару
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInSerializer
    # permission_classes = [IsAuthenticated]  # Разрешено только авторизованным пользователям

    def post(self, request, format=None, *args, **kwargs):
        self.product_id = kwargs["pk"]  # id товара

        # Создаем новый комментарий
        CommentsService.add_new_comments(
            product_id=self.product_id,
            user=request.user,
            data=request.data
        )

        comments = CommentsService.all_comments(product_id=self.product_id)  # Все комментарии товара
        serializer = ReviewOutSerializer(comments, many=True)  # Валидация данных (many=True - список)

        # Сериализуем данные и отправляем Json
        # safe=False - разрешаем сериализацию данных, не являющихся словарем (получаем список с OrderedDict)
        return JsonResponse(serializer.data, safe=False)


class LimitedProductsView(viewsets.ViewSet):
    """
    Вывод товаров ограниченной серии
    """

    @swagger_auto_schema(
        tags=['catalog'],
        responses={
            200: ProductShortSerializer(many=TagSerializer)
        }
    )
    def list(self, request):
        """
        Get catalog limeted items
        """
        logger.debug("Вывод лимитированных товаров")

        queryset = Product.objects.filter(count__lte=50)
        serializer = ProductShortSerializer(queryset, many=True)

        return JsonResponse(serializer.data, safe=False)
