from django.urls import path
from rest_framework import routers

from src.api_shop.api.product import ProductDetail, CategoriesList, TagList


urlpatterns = [
    path('product/<int:pk>/', ProductDetail.as_view(), name='product_detail'),
    path('categories/', CategoriesList.as_view(), name='categories'),
    path('tags/', TagList.as_view(), name='tags'),
]
