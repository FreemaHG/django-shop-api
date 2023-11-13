import logging

from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins, generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from src.api_shop.models import Product
from src.api_shop.serializers.payment import PaymentSerializer
from src.api_shop.tasks import payment
from src.api_shop.swagger import order_id


logger = logging.getLogger(__name__)


class PaymentView(mixins.CreateModelMixin, generics.GenericAPIView):

    # TODO Решить, что вместо этого!!!
    queryset = Product.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["payment"],
        manual_parameters=[order_id],
        request_body=PaymentSerializer(),
        responses={200: "successful operation"},
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Оплата заказа
        """
        serializer = PaymentSerializer(data=request.data)

        if serializer.is_valid():
            res = payment.delay(
                order_id=kwargs["pk"], data=serializer.validated_data
            )  # Оплата заказа в фоне (Celery)

            if res:
                return Response(status=status.HTTP_200_OK)
            return Response(
                {"message": "Ошибка при выполнении оплаты"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        else:
            logging.error(f"Невалидные данные: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
