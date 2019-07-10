# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User, Post
from django.contrib.auth.models import Group

admin.site.unregister(Group)
admin.site.register(User)
admin.site.register(Post)
