import graphene

from django.contrib.auth.models import User
from graphql import GraphQLError

from django.contrib.auth import authenticate

from core_api.auth.decorators import auth_required, has_permission
from core_api.auth.jwt_middleware import (
    JWTAuthenticationMiddleware,
    make_jwt,
    revoke_jwt,
)
from core_api.models import Audio, Song, UserFavorite
from core_api.objects.objects import SongType

from graphene_file_upload.scalars import Upload
from django.core.files.uploadedfile import TemporaryUploadedFile

from django.core.files.storage import FileSystemStorage

from core_api.utils.utils import get_object_id


class UserRegister(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=True)
        last_name = graphene.String(required=True)
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    success = graphene.Field(graphene.Boolean)

    def mutate(self, info, **kwargs):

        new_email = kwargs.get("email")
        new_username = kwargs.get("username")

        email_taken = User.objects.filter(email=new_email).exists()
        username_taken = User.objects.filter(username=new_username).exists()

        if email_taken is True:
            raise GraphQLError("This email is taken")
        if username_taken is True:
            raise GraphQLError("This username is taken")

        new_user = User.objects.create_user(**kwargs)
        new_user.save()

        return UserRegister(success=True)


class UserLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.Field(graphene.JSONString)

    def mutate(self, info, **kwargs):
        token = None

        user = authenticate(**kwargs)
        if not user:
            raise GraphQLError("Incorrect credentials")

        token = make_jwt(user)

        return UserLogin(token=token)


class UserLogout(graphene.Mutation):
    success = graphene.Boolean()

    @auth_required
    def mutate(self, info, **kwargs):

        token = JWTAuthenticationMiddleware.get_jwt_user(info.context)["decoded_token"]

        revoke_jwt(token)

        success = True

        return UserLogout(success=success)


class SongAddToFavorites(graphene.Mutation):
    class Arguments:
        song_id = graphene.ID(required=True)

    success = graphene.Boolean()

    @auth_required
    @has_permission("add_to_favorites")
    def mutate(self, info, song_id, **kwargs):

        user = JWTAuthenticationMiddleware.get_jwt_user(info.context)["user"]

        song_id = get_object_id(song_id)

        song = Song.objects.filter(id=song_id).first()

        if not song:
            raise GraphQLError("There's no song with given ID")

        UserFavorite.objects.create(user=user, song=song).save()

        return SongAddToFavorites(success=True)


class SongCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        published_at = graphene.DateTime(required=True)
        new_file = Upload(required=False)

    song = graphene.Field(SongType)

    # @auth_required
    @has_permission("create_song")
    def mutate(self, info, name, published_at, new_file=None):
        song = Song(name=name, published_at=published_at)
        # song.save()

        if new_file is not None:
            new_file: TemporaryUploadedFile = new_file

            print(new_file.temporary_file_path())

            destination = "public/media/songs/"
            fs = FileSystemStorage(location=destination)
            filename = fs.save(new_file.name, new_file)

            audio = Audio.objects.create(duration=134, waveform="fff", file=filename)
            audio.save()

            song.audio_files.add(audio)
            song.save()

        return SongCreate(song=song)
