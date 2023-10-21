from django.urls import path
from rest_framework import routers

from src.api_user.api import register_user, user_login, user_logout


urlpatterns = [
    path('in/', user_login, name='sing-in'),
    path('up/', register_user, name='sing-up'),
    path('out/', user_logout, name='sing-out'),
]

# router = routers.SimpleRouter()
#
# router.register(r'sing-out', LogoutUserView, basename='sing-out')
# urlpatterns += router.urls