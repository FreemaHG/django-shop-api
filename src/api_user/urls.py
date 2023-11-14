from django.urls import path, include

from src.api_user.api.auth import register_user, user_login, user_logout
from src.api_user.api.profile import update_avatar, update_password, ProfileView


urlpatterns = [
    # Регистрация, авторизация, выход из учетной записи
    path(
        "sign-",
        include(
            [
                path("in/", user_login, name="sign-in"),
                path("up/", register_user, name="sign-up"),
                path("out/", user_logout, name="sign-out"),
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
