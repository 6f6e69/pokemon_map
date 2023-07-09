from django.db import models  # noqa F401


class Pokemon(models.Model):
    title: models.CharField = models.CharField(max_length=200)
    image: models.ImageField = models.ImageField(blank=True)

    def __str__(self) -> str:
        return self.title


class PokemonEntity(models.Model):
    latitude: models.FloatField = models.FloatField(verbose_name='Lat')
    longitude: models.FloatField = models.FloatField(verbose_name='Lon')
    pokemon: models.ForeignKey = models.ForeignKey(Pokemon,
                                                   on_delete=models.CASCADE,
                                                   verbose_name="pokemon")
    appeared_at: models.DateTimeField = models.DateTimeField(blank=True,
                                                             null=True)
    disappeared_at: models.DateTimeField = models.DateTimeField(blank=True,
                                                                null=True)
    level: models.IntegerField = models.IntegerField(blank=True,
                                                     null=True)
    health: models.IntegerField = models.IntegerField(blank=True,
                                                      null=True)
    strength: models.IntegerField = models.IntegerField(blank=True,
                                                        null=True)
    defence: models.IntegerField = models.IntegerField(blank=True,
                                                       null=True)
    stamina: models.IntegerField = models.IntegerField(blank=True,
                                                       null=True)

    def __str__(self) -> str:
        return (f"{self.pokemon.title} {self.level}lvl "
                f"{self.latitude,self.longitude}")
