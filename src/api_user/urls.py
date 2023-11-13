from django.urls import path, include

from src.api_user.api.auth import register_user, user_login, user_logout
from src.api_user.api.profile import update_avatar, update_password, ProfileView


urlpatterns = [
    # Регистрация, авторизация, выход из учетной записи
    path(
        "sign-",
        include(
            [
                path("in/", user_login, name="sing-in"),
                path("up/", register_user, name="sing-up"),
                path("out/", user_logout, name="sing-out"),
            ]
        ),
    ),
    # Профайл
    path(
        "profile/",
        include(
            [
                path("password/", update_password, name="update-password"),
                path("avatar/", update_avatar, name="update-profile"),
                path("", ProfileView.as_view(), name="profile"),
            ]
        ),
    ),
]
