import graphene

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from graphql import GraphQLError

from core_api.models import Audio, Song
from core_api.objects.objects import SongType

from graphene_file_upload.scalars import Upload
from django.core.files.uploadedfile import TemporaryUploadedFile

from django.core.files.storage import FileSystemStorage


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


# class UserLogin(graphene.Mutation):


class SongCreate(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        published_at = graphene.DateTime(required=True)
        new_file = Upload(required=True)

    song = graphene.Field(SongType)

    def mutate(self, info, name, published_at, new_file):

        new_file: TemporaryUploadedFile = new_file

        print(new_file.temporary_file_path())

        destination = "public/media/songs/"
        fs = FileSystemStorage(location=destination)
        filename = fs.save(new_file.name, new_file)

        audio = Audio.objects.create(duration=134, waveform="fff", file=filename)
        audio.save()

        song = Song(name=name, published_at=published_at)
        song.save()

        song.audio_files.add(audio)
        song.save()

        return SongCreate(song=song)
