from django.db import models
from django.contrib.auth import get_user_model


class Genre(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=60)

    def save(self, *args, **kwargs):
        val = getattr(self, "name", False)
        if val:
            setattr(self, "name", val.title())
        super(Genre, self).save(*args, **kwargs)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
