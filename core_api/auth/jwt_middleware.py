from ast import Dict
from graphql import GraphQLError
import jwt
import traceback
import hashlib
import base64
from datetime import datetime, timedelta
from time import time

from django.utils.functional import SimpleLazyObject
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser, User
from django.conf import LazySettings
from django.contrib.auth.middleware import get_user

from django_redis import get_redis_connection

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

    encoded = jwt.encode(payload, secret, algorithm="HS256")

    return encoded


def revoke_jwt(token: str):
    token_key = f"token:{token['jti']}"
    token_expires = token["exp"]

    expire_ts = round(int(token_expires) - time())

    try:
        redis = get_redis_connection()
        redis.hset(token_key, mapping={"revoked": "true"})
        redis.expire(token_key, expire_ts)
    except Exception as e:
        return False

    return True


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = SimpleLazyObject(
            lambda: self.__class__.get_jwt_user(request)["user"]
        )

    @staticmethod
    def get_jwt_user(request):
        user = get_user(request)
        token = request.META.get("HTTP_AUTHORIZATION", None)

        if user.is_authenticated and token is None:
            return {"user": user, "decoded_token": None}

        user_jwt = None

        user = AnonymousUser()
        if token is not None:
            try:
                user_jwt = jwt.decode(token, settings.JWT_SECRET, algorithms="HS256")
                jti = user_jwt["jti"]

                redis = get_redis_connection()
                revoked_token: Dict = redis.hgetall(f"token:{jti}")

                if (
                    revoked_token is not None
                    and revoked_token.get(b"revoked") == b"true"
                ):
                    raise GraphQLError("Your token had been revoked")

                user = User.objects.get(username=user_jwt["context"]["username"])
            except GraphQLError as e:
                raise GraphQLError(e.message)
            except Exception as e:
                traceback.print_exc()
                raise GraphQLError(e)

        return {"user": user, "decoded_token": user_jwt}
