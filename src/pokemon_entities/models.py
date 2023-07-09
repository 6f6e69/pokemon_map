from django.db import models  # noqa F401
from django.utils.timezone import localtime
from datetime import tzinfo


class Pokemon(models.Model):
    title = models.CharField(max_length=200,
                             verbose_name="название (русское)")
    title_en = models.CharField(max_length=200,
                                blank=True,
                                default="",
                                verbose_name="название (английское)")
    title_jp = models.CharField(max_length=200,
                                blank=True,
                                default="",
                                verbose_name="название (японское)")
    image = models.ImageField(verbose_name="изображение")
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.SET_NULL,
                                           blank=True,
                                           null=True,
                                           verbose_name="предыдущая эволюция")
    description = models.TextField(blank=True,
                                   default="",
                                   verbose_name="описание")

    def __str__(self) -> str:
        return self.title

    class Meta:
        verbose_name = "покемон"
        verbose_name_plural = "покемоны"


class PokemonEntity(models.Model):
    latitude = models.FloatField(verbose_name="широта")
    longitude = models.FloatField(verbose_name="долгота")
    pokemon = models.ForeignKey(Pokemon,
                                on_delete=models.CASCADE,
                                verbose_name="покемон")
    appeared_at = models.DateTimeField(verbose_name="появится с")
    disappeared_at = models.DateTimeField(verbose_name="исчезнет в")
    level = models.IntegerField(blank=True,
                                null=True,
                                verbose_name="уровень")
    health = models.IntegerField(blank=True,
                                 null=True,
                                 verbose_name="здоровье")
    strength = models.IntegerField(blank=True,
                                   null=True,
                                   verbose_name="сила")
    defence = models.IntegerField(blank=True,
                                  null=True,
                                  verbose_name="защита")
    stamina = models.IntegerField(blank=True,
                                  null=True,
                                  verbose_name="выносливость")

    def __str__(self) -> str:
        return (f"{self.pokemon.title} {self.level}lvl "
                f"{self.latitude,self.longitude}")

    def is_active_in_timezone(self, timezone: tzinfo) -> bool:
        if self.appeared_at and self.disappeared_at:
            return (self.appeared_at <
                    localtime(timezone=timezone) <
                    self.disappeared_at)
        return False

    class Meta:
        verbose_name = "объект покемона"
        verbose_name_plural = "объекты покемонов"
