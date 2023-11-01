from rest_framework import serializers


class PaginationSerializerMixin(serializers.Serializer):
    """
    Схема добавляет поля текущей и последней страницы при разбивке результатов товаров на страницы
    """
    currentPage = serializers.IntegerField()
    lastPage = serializers.IntegerField()

    class Meta:
        fields = '__all__'
