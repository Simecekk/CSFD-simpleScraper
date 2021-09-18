from django.contrib import admin
from core.models import Actor, Movie


class ActorAdmin(admin.ModelAdmin):
    pass


class MovieAdmin(admin.ModelAdmin):
    pass


admin.site.register(Actor, ActorAdmin)
admin.site.register(Movie, MovieAdmin)
