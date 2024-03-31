import graphene

from core_api.models import Audio, Song
from core_api.objects.objects import SongType

from graphene_file_upload.scalars import Upload
from django.core.files.uploadedfile import TemporaryUploadedFile

from django.core.files.storage import FileSystemStorage


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
