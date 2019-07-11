# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Post
from django.contrib.auth.models import Group


class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Basic Information", {"fields": ["username", "email", ]}),
        ("Location", {"fields": ["latitude",
                                 "longitude", "search_distance", ]}),
        ("Account Type", {"fields": ["account", ]})
    ]
    list_display = ("username", "id", "last_login",
                    "date_joined", "email", "account",)


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
admin.site.register(Post)
