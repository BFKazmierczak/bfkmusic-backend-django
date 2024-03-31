from django_filters import FilterSet, CharFilter

from core_api.models import Song


class SongFilter(FilterSet):
    name = CharFilter(lookup_expr=["iexact"])

    class Meta:
        model = Song
        fields = ["id"]
