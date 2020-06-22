from shorty.schema import QueryClass, Mutation

import graphene

class Query(QueryClass, graphene.ObjectType):
    pass

class Mutation(Mutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)