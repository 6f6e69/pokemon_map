from django.db import models  # noqa F401


class Pokemon(models.Model):
    title: models.CharField = models.CharField(max_length=200)
    image: models.ImageField = models.ImageField(blank=True)

    def __str__(self) -> str:
        return self.title


class PokemonEntity(models.Model):
    latitude: models.FloatField = models.FloatField(verbose_name='Lat')
    longitude: models.FloatField = models.FloatField(verbose_name='Lon')
