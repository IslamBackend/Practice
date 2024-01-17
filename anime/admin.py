from django.contrib import admin
from anime.models import Anime, Comment, HashTag


admin.site.register(Anime)
admin.site.register(Comment)
admin.site.register(HashTag)
