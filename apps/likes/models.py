from django.db import models

from apps.room.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()


class Like(models.Model):
    owner = models.ForeignKey(User, related_name='likes', on_delete=models.CASCADE)
    post = models.ForeignKey(Room, related_name='likes', on_delete=models.CASCADE)
    is_liked = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.is_liked} --> {self.post}'

