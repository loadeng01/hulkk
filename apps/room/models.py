from django.db import models
from apps.category.models import Category


class Room(models.Model):
    class RoomStatus(models.TextChoices):
        free = 'free'
        busy = 'busy'
        reserved = 'reserved'

    number = models.IntegerField()
    count_rooms = models.IntegerField()
    # category = models.ForeignKey(Category, related_name='rooms', on_delete=models.CASCADE)
    state = models.CharField(max_length=8, choices=RoomStatus, default=RoomStatus.free)
    preview = models.ImageField(upload_to='previews/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Номер'
        verbose_name_plural = 'Номера'

    def __str__(self):
        return f'{self.number} (rooms:{self.count_rooms})'


class RoomImages(models.Model):
    image = models.ImageField(upload_to='rooms/')
    post = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        return super(RoomImages, self).save(*args, **kwargs)


