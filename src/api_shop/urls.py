from django.urls import path, include
from rest_framework import routers

from src.api_shop.api.tag import TagListView

from src.api_shop.api.product import (
    ProductDetailView,
    ReviewCreateView,
)

from src.api_shop.api.catalog import (
    CategoriesListView,
    LimitedProductsView,
    BannersProductsView,
    PopularProductsView,
    SalesView,
    CatalogView,
)

from src.api_shop.api.basket import BasketView


urlpatterns = [
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('product/', include([
        path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
        path('<int:pk>/reviews/', ReviewCreateView.as_view(), name='create-review'),
    ])),
    path('basket/', BasketView.as_view(), name='basket'),
]


router = routers.SimpleRouter()
# ВАЖНО: т.к. в представлениях нет queryset / get_queryset(), то basename обязательно!
router.register(r'products/limited', LimitedProductsView, basename='limited-products')
router.register(r'banners', BannersProductsView, basename='banner')
router.register(r'products/popular', PopularProductsView, basename='popular-products')
router.register(r'sales', SalesView, basename='sales')
router.register(r'catalog', CatalogView, basename='catalog')
router.register(r'tags', TagListView, basename='tags')
# router.register(r'basket', BasketView, basename='basket')

urlpatterns += router.urls
