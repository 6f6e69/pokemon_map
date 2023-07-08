from django.contrib import admin
from .models import Pokemon, PokemonEntity


class PokemonAdmin(admin.ModelAdmin):
    pass


class PokemonEntityAdmin(admin.ModelAdmin):
    pass


admin.site.register(Pokemon)
admin.site.register(PokemonEntity)
