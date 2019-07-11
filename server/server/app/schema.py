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


class SignupMutation(graphene.Mutation):
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    user = graphene.Field(UserType)

    def mutate(self, info, *args, **kwargs):
        try:
            new_user = User.objects.create(
                username=kwargs.get("username"),
                email=kwargs.get("email"),
                password=kwargs.get("password")
            )
            new_user.save()
            
            return SignupMutation(user=new_user)
        except:
            raise Exception('Invalid user credentials') 


class Mutation(graphene.ObjectType):
    signup = SignupMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
