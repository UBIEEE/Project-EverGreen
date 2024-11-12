from django.contrib import admin

from eg_app.models import Comments, Post

admin.site.register(Post)
admin.site.register(Comments)
