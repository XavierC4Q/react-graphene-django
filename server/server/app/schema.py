import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Post

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', 'account', )

class Query(graphene.ObjectType):
    user = graphene.Field(UserType, user_id=graphene.Int())
    users = graphene.List(UserType)

    def resolve_user(self, info, user_id):
        return User.objects.get(id=user_id)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

schema = graphene.Schema(query=Query)