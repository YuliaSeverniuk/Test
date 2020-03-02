from django.contrib import admin

from .models import Posts, Likes

admin.site.register(Posts)
admin.site.register(Likes)