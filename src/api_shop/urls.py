from django.urls import path, include
from rest_framework import routers

from src.api_shop.api.product import (
    ProductDetailView,
    CategoriesListView,
    TagListView,
    ReviewCreateView,
    LimitedProductsView,
)

urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('tags/', TagListView.as_view(), name='tags'),
    path('product/', include([
        path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
        path('<int:pk>/reviews/', ReviewCreateView.as_view(), name='create-review'),
    ])),
    # path('products/', include([
    #     path('limited/', LimitedProductsView.as_view(), name='limited-products')
    # ])),
]


# TODO Убрать, если не используется
router = routers.SimpleRouter()
# Можно передать атрибут basename для обозначения urlname,
# в противном случае оно генерируется на базе queryset представдления
router.register(r'products/limited', LimitedProductsView, basename='limited-products')
urlpatterns += router.urls
