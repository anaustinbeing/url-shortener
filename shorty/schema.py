from .models import URL

import graphene
from graphene_django import DjangoObjectType

class URLType(DjangoObjectType):
    class Meta:
        model = URL

# Query purpose.
class QueryClass(graphene.ObjectType):
    urls = graphene.List(URLType, contains=graphene.String())

    def resolve_urls(self, arg, contains=None, **info):
        if contains:
            return URL.objects.filter(original_url__icontains=contains)
        return URL.objects.all()

# Create purpose.
class CreateURL(graphene.Mutation):
    url = graphene.Field(URLType)

    class Arguments:
        full_url = graphene.String()

    def mutate(self, info, full_url):
        url = URL(original_url=full_url)
        url.save()
        return CreateURL(url=url)

class Mutation(graphene.ObjectType):
    create_url = CreateURL.Field()