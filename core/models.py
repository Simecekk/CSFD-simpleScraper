from django.db import models


class BaseModel(models.Model):
    created = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    modified = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    change_log_menu_mixin = NotImplemented

    class Meta:
        abstract = True


class Movie(BaseModel):
    name = models.CharField(max_length=512)
    detail_url = models.URLField(unique=True)
    actors = models.ManyToManyField(
        'core.Actor',
        blank=True,
        related_name='movies',
    )

    def __str__(self):
        return f'{self.id} : {self.name}'


class Actor(BaseModel):
    name = models.CharField(max_length=256)
    detail_url = models.URLField(unique=True)

    def __str__(self):
        return f'{self.id} : {self.name}'
