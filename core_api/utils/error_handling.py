import graphene
from graphql import GraphQLError, Node, Source
from graphql.error.graphql_error import GraphQLErrorExtensions


class ErrorEnum(graphene.Enum):
    NO_LIBRARY = {
        "message": "Library not found",
        "extensions": {
            "code": "NO_LIBRARY",
            "toast": False,
            "render": "Wygląda na to, że nie posiadasz jeszcze biblioteki. Po zakupie pierwszego utworu, pojawi się on tutaj.",
        },
    }

    BAD_CREDENTIALS = {
        "message": "Incorrect credentials",
        "extensions": {
            "code": "BAD_CREDENTIALS",
            "toast": False,
            "render": "Niepoprawne dane logowania",
        },
    }

    USERNAME_TAKEN = {
        "message": "Provided username is taken",
        "extensions": {
            "code": "USERNAME_TAKEN",
            "toast": False,
            "render": "Nazwa użytkownika jest zajęta",
        },
    }

    EMAIL_TAKEN = {
        "message": "Provided email is taken",
        "extensions": {
            "code": "EMAIL_TAKEN",
            "toast": False,
            "render": "Podany email jest zajęty",
        },
    }

    NO_SONG = {
        "message": "No song with given ID",
        "extensions": {
            "code": "NO_SONG",
            "toast": True,
            "render": "Taki utwór nie istnieje",
        },
    }

    NOT_THE_OWNER = {
        "message": "No permission to modify this object",
        "extensions": {
            "code": "NOT_THE_OWNER",
            "toast": True,
        },
    }


class CustomGraphQLError(GraphQLError):
    def __init__(self, error: ErrorEnum) -> None:

        err_value = error.value

        message = err_value.get("message", None)
        extensions = err_value.get("extensions", None)

        # nodes, source, positions, path, original_error,
        super().__init__(message=message, extensions=extensions)
