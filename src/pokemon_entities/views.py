import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime
from .models import Pokemon, PokemonEntity
from pytz import timezone


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    map_timezone = timezone('Europe/Moscow')
    current_datetime = localtime(timezone=map_timezone)
    pokemon_entities = PokemonEntity.objects.filter(
                            appeared_at__lt=current_datetime,
                            disappeared_at__gt=current_datetime)
    for pokemon_entity in pokemon_entities:
        pokemon_image_url: str = request.build_absolute_uri(
                                     pokemon_entity.pokemon.image.url)
        add_pokemon(folium_map,
                    lat=pokemon_entity.latitude,
                    lon=pokemon_entity.longitude,
                    image_url=pokemon_image_url)

    pokemons = Pokemon.objects.all()

    pokemons_on_page = []

    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.image.url),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    pokemon_characteristics = {
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': request.build_absolute_uri(pokemon.image.url),
        'description': pokemon.description,
    }

    if pokemon.previous_evolution:
        pokemon_characteristics['previous_evolution'] = {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(
                       pokemon.previous_evolution.image.url)
        }

    next_evolution = pokemon.prev_evolut.first()
    if next_evolution:
        pokemon_characteristics['next_evolution'] = {
            'pokemon_id': next_evolution.id,
            'title_ru': next_evolution.title,
            'img_url': request.build_absolute_uri(
                       next_evolution.image.url)
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_entities = PokemonEntity.objects.filter(pokemon__id=pokemon_id)
    for pokemon_entity in pokemon_entities:
        pokemon_image_url = request.build_absolute_uri(
                                         pokemon_entity.pokemon.image.url)
        add_pokemon(
            folium_map,
            pokemon_entity.latitude,
            pokemon_entity.longitude,
            pokemon_image_url,
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_characteristics
    })
