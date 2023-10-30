from django.urls import path, include
from rest_framework import routers

from src.api_shop.api.product import (
    ProductDetailView,
    CategoriesListView,
    TagListView,
    ReviewCreateView,
    LimitedProductsView,
    BannersProductsView,
    PopularProductsView,
    SalesView,
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


router = routers.SimpleRouter()
# ВАЖНО: т.к. в представлениях нет queryset / get_queryset(), то basename обязательно!
router.register(r'products/limited', LimitedProductsView, basename='limited-products')
router.register(r'banners', BannersProductsView, basename='banner')
router.register(r'products/popular', PopularProductsView, basename='popular-products')
router.register(r'sales', SalesView, basename='sales')

urlpatterns += router.urls
