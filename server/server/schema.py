import graphene
import graphql_jwt

from .app import schema as appSchema
from .app.schema import UserType


class Query(
    appSchema.Query,
    graphene.ObjectType
):
    pass

#Add user to token request
class ObtainJSONWebToken(graphql_jwt.JSONWebTokenMutation):
    user = graphene.Field(UserType)

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user)

class Mutation(
    appSchema.Mutation,
    graphene.ObjectType
):
    get_token = ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
