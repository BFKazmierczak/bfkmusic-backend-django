from django_filters import FilterSet, CharFilter, OrderingFilter

from core_api.models import Song


class SongFilter(FilterSet):
    class Meta:
        model = Song
        fields = ["id"]

    name = CharFilter(lookup_expr=["iexact"])
    order_by = OrderingFilter(fields=("published_at", "name"))
