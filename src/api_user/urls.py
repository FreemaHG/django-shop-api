from django.urls import path, include
from rest_framework import routers

from src.api_user.api.register_login_logout import register_user, user_login, user_logout
from src.api_user.api.profile import profile


urlpatterns = [
    # Регистрация, авторизация, выход из учетной записи
    path('sign-', include([
        path('in/', user_login, name='sing-in'),
        path('up/', register_user, name='sing-up'),
        path('out/', user_logout, name='sing-out'),
    ])),
    # Профайл
    path('profile/', include([
        path('', profile, name='profile'),
        # 'password/',
        # 'avatar/',
    ]))

]

# router = routers.SimpleRouter()
#
# router.register(r'profile', ProfileViewSet, basename='profile')
# urlpatterns += router.urls