from django.contrib.auth import get_user_model
import graphene
from graphene_django.types import DjangoObjectType
from .models import User, Post


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password', 'account', )

class PostType(DjangoObjectType):
    class Meta:
        model = Post


class Query(graphene.ObjectType):
    user = graphene.Field(UserType, user_id=graphene.Int())
    users = graphene.List(UserType)
    post = graphene.Field(PostType, post_id=graphene.Int())
    posts = graphene.List(PostType)
    user_posts = graphene.List(PostType, user_id=graphene.Int())

    def resolve_user(self, info, user_id):
        return User.objects.get(id=user_id)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_post(self, info, post_id):
        return Post.objects.get(id=post_id)

    def resolve_posts(self, info):
        return Post.objects.all()

    def resolve_user_posts(self, info, user_id):
        return Post.objects.get(user__id=user_id, many=True)


class SignupMutation(graphene.Mutation):
    new_user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, *args, **kwargs):
        try:
            new_user = get_user_model()(
                username=kwargs.get('username'),
                email=kwargs.get('email'),
            )
            new_user.set_password(kwargs.get('password'))
            new_user.save()

            return SignupMutation(new_user=new_user)
        except:
            raise Exception('Invalid user credentials')


class EditUserMutation(graphene.Mutation):
    edited_user = graphene.Field(UserType)

    class Arguments:
        id = graphene.Int(required=True)
        username = graphene.String()
        email = graphene.String()
        password = graphene.String()
        latitude = graphene.Decimal()
        longitude = graphene.Decimal()

    def mutate(self, info, *args, **kwargs):
        try:
            user = User.objects.get(id=kwargs.get('id'))

            if user is None:
                raise Exception('User does not exist')

            if kwargs.get('password'):
                user.set_password(kwargs.get('password'))

            if kwargs.get('username'):
                user.username = kwargs.get('username')

            if kwargs.get('email'):
                user.email = kwargs.get('email')

            if kwargs.get('latitude'):
                user.latitude = kwargs.get('latitude')

            if kwargs.get('longitude'):
                user.longitude = kwargs.get('longitude')

            user.save()
            return EditUserMutation(edited_user=user)
        except:
            raise Exception('Failed to edit user')


class Mutation(graphene.ObjectType):
    signup = SignupMutation.Field()
    edit_user = EditUserMutation.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
