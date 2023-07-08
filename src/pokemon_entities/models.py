from django.db import models  # noqa F401


class Pokemon(models.Model):
    title: models.CharField = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.title
