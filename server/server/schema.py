import graphene
import graphql_jwt

from .app import schema as appSchema


class Query(
    appSchema.Query,
    graphene.ObjectType
):
    pass


class Mutation(
    appSchema.Mutation,
    graphene.ObjectType
):
    get_token = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
