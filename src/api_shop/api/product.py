import logging

from django.http import JsonResponse
from rest_framework.generics import RetrieveAPIView, GenericAPIView
from rest_framework.mixins import CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from src.api_shop.models.product import Product
from src.api_shop.models.review import Review
from src.api_shop.serializers.product import ProductFullSerializer
from src.api_shop.serializers.review import ReviewInSerializer, ReviewOutSerializer
from src.api_shop.services.comment import CommentsService


logger = logging.getLogger(__name__)


class ProductDetailView(RetrieveAPIView):
    """
    Вывод данных о товаре (по pk в url)
    """
    queryset = Product.objects.prefetch_related("reviews").filter(deleted=False)  # Активные товары
    serializer_class = ProductFullSerializer


class ReviewCreateView(CreateModelMixin, GenericAPIView):
    """
    Добавление отзыва к товару
    """
    queryset = Review.objects.all()
    serializer_class = ReviewInSerializer
    permission_classes = [IsAuthenticated]  # Разрешено только авторизованным пользователям

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
