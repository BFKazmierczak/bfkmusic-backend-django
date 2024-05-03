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
from core_api.models import Audio, Comment, Song, UserFavorite
from core_api.objects.objects import AudioType, CommentType, SongType, UserType

from graphene_file_upload.scalars import Upload
from django.core.files.uploadedfile import TemporaryUploadedFile

from django.core.files.storage import FileSystemStorage

from core_api.utils.error_handling import CustomGraphQLError, ErrorEnum
from core_api.utils.utils import get_object_id, song_in_library


class UserRegister(graphene.Mutation):
    class Arguments:
        first_name = graphene.String(required=False)
        last_name = graphene.String(required=False)
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
            raise CustomGraphQLError(ErrorEnum.EMAIL_TAKEN)
        if username_taken is True:
            raise CustomGraphQLError(ErrorEnum.USERNAME_TAKEN)

        new_user = User.objects.create_user(**kwargs)
        new_user.save()

        return UserRegister(success=True)


class UserLogin(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.String()
    user = graphene.Field(UserType)

    def mutate(self, info, **kwargs):
        token = None

        user = authenticate(**kwargs)
        if not user:
            raise CustomGraphQLError(ErrorEnum.BAD_CREDENTIALS)

        token = make_jwt(user)

        return UserLogin(token=token, user=user)


class UserLogout(graphene.Mutation):
    success = graphene.Boolean()

    @auth_required
    def mutate(self, info, **kwargs):

        token = JWTAuthenticationMiddleware.get_jwt_user(info.context)["decoded_token"]

        revoke_jwt(token)

        success = True

        return UserLogout(success=success)


class SongManageFavorite(graphene.Mutation):
    class Arguments:
        song_id = graphene.ID(required=True)

    success = graphene.Boolean()
    song = graphene.Field(SongType)

    @auth_required
    @has_permission("add_to_favorites")
    def mutate(self, info, song_id, **kwargs):

        user = info.context.user

        song_id = get_object_id(song_id)

        song = Song.objects.filter(id=song_id).first()

        if not song:
            raise CustomGraphQLError(ErrorEnum.NO_SONG)

        favorite_song = UserFavorite.objects.filter(user=user, song=song).first()
        if favorite_song is None:
            favorite_song = UserFavorite.objects.create(user=user, song=song).save()
        else:
            UserFavorite.objects.delete(favorite_song)

        return SongManageFavorite(success=True, song=favorite_song)


class CommentCreate(graphene.Mutation):
    class Arguments:
        song_id = graphene.ID(required=True)
        content = graphene.String(required=True)
        start_time = graphene.Int(required=True)
        end_time = graphene.Int(required=True)

    comment = graphene.Field(CommentType)

    @auth_required
    def mutate(self, info, song_id, **kwargs):
        user = info.context.user

        song_id = get_object_id(song_id)

        song = Song.objects.filter(id=song_id).first()
        if song is None:
            raise CustomGraphQLError(ErrorEnum.NO_SONG)

        if not song_in_library(user, song_id):
            raise CustomGraphQLError(ErrorEnum.NOT_THE_OWNER)

        comment = Comment(song=song, user=user, **kwargs)
        comment.save()

        return CommentCreate(comment=comment)


class SongCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        published_at = graphene.DateTime(required=True)
        new_file = Upload(required=False)

    song = graphene.Field(SongType)

    @auth_required
    @has_permission("create_song")
    def mutate(self, info, name, published_at, new_file=None):
        song = Song(name=name, published_at=published_at)

        if new_file is not None:
            new_file: TemporaryUploadedFile = new_file

            destination = "public/media/songs/"
            fs = FileSystemStorage(location=destination)
            filename = fs.save(new_file.name, new_file)

            audio = Audio.objects.create(duration=0, waveform=[0], file=filename)
            audio.save()

            song.audio_files.add(audio)
            song.save()

        return SongCreate(song=song)


class SongUploadVersion(graphene.Mutation):
    class Arguments:
        song_id = graphene.ID(required=True)
        audio_file = Upload(required=True)

    audio = graphene.Field(AudioType)

    @auth_required
    @has_permission("create_audio")
    def mutate(self, info, song_id, audio_file, **kwargs):

        user = info.context.user

        song_id = get_object_id(song_id)

        song = Song.objects.filter(id=song_id).first()
        if song is None:
            raise CustomGraphQLError(ErrorEnum.NO_SONG)

        if not song_in_library(user, song_id):
            raise CustomGraphQLError(ErrorEnum.NOT_THE_OWNER)

        audio_file: TemporaryUploadedFile = audio_file

        destination = "public/media/songs/"
        fs = FileSystemStorage(location=destination)
        filename = fs.save(audio_file.name, audio_file)

        audio = Audio.objects.create(file=f"songs/{filename}", uploaded_by=user)

        audio.save()

        song.audio_files.add(audio)
        song.save()

        return SongUploadVersion(audio=audio)
