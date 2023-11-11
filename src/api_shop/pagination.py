import math

from rest_framework import pagination
from rest_framework.response import Response


class CustomPagination(pagination.PageNumberPagination):
    """
    Кастомная пагинация
    """
    page_query_param = 'currentPage'  # http://127.0.0.1:8000/api/sales/?currentPage=2'

    def get_paginated_response(self, data):
        return Response({
            'items': data,  # Результат с данными запроса
            # Текущая страница (извлекаем значение currentPage из URL, по умолчанию 1)
            'currentPage': int(self.request.query_params.get(self.page_query_param, 1)),
            # Последняя страница (кол-во записей / кол-во записей на 1 странице, округление в большую сторону)
            'lastPage': math.ceil(self.page.paginator.count / self.page_size)
        })


class SalePagination(CustomPagination):
    """
    Пагинация для товаров на распродаже
    """
    page_size = 12  # Кол-во записей на странице


class CatalogPagination(CustomPagination):
    """
    Пагинация для каталога
    """
    page_size = 8  # Кол-во записей на странице
