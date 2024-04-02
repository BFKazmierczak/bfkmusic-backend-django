import jwt
import traceback
import hashlib
import base64
from datetime import datetime, timedelta

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser, User
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user

settings = LazySettings()


def make_jwt(user: User):
    expiration_date = datetime.now() + timedelta(hours=1)

    payload = {
        "iss": "bfkmusic",
        "exp": expiration_date,
        "context": {
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "groups": [],
        },
    }

    jti_hash = hashlib.sha256(payload.__str__().encode("utf-8")).digest()

    payload["jti"] = base64.b64encode(jti_hash).__str__()

    secret = settings.JWT_SECRET
    if not isinstance(secret, str):
        raise Exception("Incorrect jwt secret")

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
