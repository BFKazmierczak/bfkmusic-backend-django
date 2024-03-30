import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from django_filters import FilterSet, CharFilter

from polls.models import Choice, Question


class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        interfaces = (graphene.relay.Node,)


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        interfaces = (graphene.relay.Node,)


class QuestionFilter(FilterSet):
    name = CharFilter(lookup_expr=["iexact"])

    class Meta:
        model = Question
        fields = ["id"]


class Query(graphene.ObjectType):
    all_questions = DjangoFilterConnectionField(
        QuestionType, filterset_class=QuestionFilter
    )
    all_choices = graphene.List(ChoiceType)


schema = graphene.Schema(query=Query)
