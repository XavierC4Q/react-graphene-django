from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator


class User(AbstractUser):
    account_creator = "CREATOR"
    account_influencer = "INFLUENCER"
    account_standard = "STANDARD USER"

    username = models.CharField(
        max_length=21,
        unique=True,
        blank=False,
        null=False,
        validators=[MinLengthValidator(
            6, message="Username must be at least 6 characters")])
    email = models.EmailField(unique=True, blank=False, null=False)
    account = models.CharField(
        max_length=20,
        choices=(
            (account_creator, "Creator"),
            (account_influencer, "Influencer"),
            (account_standard, "Standard User")),
        default=account_standard)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=40.7128)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=74.0060)
    search_distance = models.IntegerField(default=5)

    def __str__(self):
        return f"User: {self.id}, username: {self.username}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_user")
    title = models.CharField(max_length=50, blank=False, null=False)
    content = models.CharField(max_length=300, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Post: {self.id}, title: {self.title}"