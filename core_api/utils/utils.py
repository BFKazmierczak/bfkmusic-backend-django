from graphql_relay import from_global_id
from django.contrib.auth.models import User

from core_api.models import UserLibrary


def song_in_library(user: User, song_id: int):
    library_exists = UserLibrary.objects.filter(user_id=user.id).exists()
    if library_exists is False or not user.library.songs.filter(id=song_id).exists():
        return False

    return True


def get_object_id(global_id):

    object_id = from_global_id(global_id).id

    if len(object_id) == 0:
        raise Exception("Incorrect global ID was provided.")

    return object_id
