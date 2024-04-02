import jwt
import traceback

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser, User
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user

settings = LazySettings()


def make_jwt(user: User):

    payload = {
        "username": user.username,
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    encoded = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return encoded


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda: self.__class__.get_jwt_user(request))

    @staticmethod
    def get_jwt_user(request):
        user_jwt = get_user(request)
        if user_jwt.is_authenticated:
            return user_jwt
        token = request.META.get("HTTP_AUTHORIZATION", None)

        print(f"Token: {token}")

        user_jwt = AnonymousUser()
        if token is not None:
            try:
                user_jwt = jwt.decode(token, settings.JWT_SECRET, algorithms="HS256")

                print(f"JWT: {user_jwt}")

                user_jwt = User.objects.get(username=user_jwt["username"])
                print(f"Found user: {user_jwt}")
            except Exception as e:  # NoQA
                traceback.print_exc()

        print(f"Is authenticated?: {user_jwt.is_authenticated}")
        return user_jwt
