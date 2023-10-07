from django.urls import path
from rest_framework import routers

from src.api_shop.api.product import (
    ProductDetailView,
    CategoriesListView,
    TagListView,
    ReviewCreateView
)

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/<int:pk>/reviews/', ReviewCreateView.as_view(), name='create_review'),
]


# TODO Убрать, если не используется
# router = routers.SimpleRouter()
# Можно передать атрибут basename для обозначения urlname,
# в противном случае оно генерируется на базе queryset представдления
# router.register(r'categories', CategoriesList)
# urlpatterns = router.urls
# urlpatterns += router.urls
