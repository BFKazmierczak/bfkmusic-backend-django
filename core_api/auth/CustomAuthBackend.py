from typing import Any
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http import HttpRequest


class CustomAuthBackend(BaseBackend):
    def authenticate(
        self,
        request: HttpRequest,
        username: str | None = ...,
        password: str | None = ...,
        **kwargs: Any
    ) -> AbstractBaseUser | None:
        return super().authenticate(request, username, password, **kwargs)

    def get_user(self, user_id: int) -> AbstractBaseUser | None:
        return super().get_user(user_id)
