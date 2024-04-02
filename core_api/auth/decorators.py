from functools import wraps

from django.contrib.auth.models import User

from graphql import GraphQLError


def auth_required(func):
    @wraps(func)
    def wrapper(self, info, **kwargs):

        request = info.context
        if not request.user.is_authenticated:
            raise GraphQLError("This action requires logging in")

        func(self, info, **kwargs)

    return wrapper


def has_permission(perm: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, info, **kwargs):
            print(f"checking for: {perm}")

            user = info.context.user
            if not user.is_authenticated:
                raise GraphQLError("This action requires logging in")

            user: User = user

            if not user.has_perm(perm):
                raise GraphQLError("Permission denied")

            func(self, info, **kwargs)

        return wrapper

    return decorator
