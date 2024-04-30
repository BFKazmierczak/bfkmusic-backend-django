from functools import wraps

from django.contrib.auth.models import User

from graphql import GraphQLError


def auth_required(func):
    @wraps(func)
    def wrapper(self, info, **kwargs):
        request = info.context
        if not request.user.is_authenticated:
            raise GraphQLError("This action requires logging in")

        return func(self, info, **kwargs)

    return wrapper


def has_permission(perm: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, info, **kwargs):
            user = info.context.user
            if not user.is_authenticated:
                raise GraphQLError("This action requires logging in")

            user: User = user

            group_has_perm = False
            for group in user.groups.all():
                if group_has_perm is True:
                    break

                for permission in group.permissions.all():
                    if permission.codename == perm:
                        group_has_perm = True
                        break

            if not user.has_perm(perm, user) and group_has_perm is False:
                raise GraphQLError("Permission denied")

            return func(self, info, **kwargs)

        return wrapper

    return decorator
