from django.db import models


class Room(models.Model):
    class RoomStatus(models.TextChoices):
        free = 'free'
        busy = 'busy'

    number = models.IntegerField()
    count_rooms = models.IntegerField()
    state = models.CharField(max_length=5, choices=RoomStatus, default=RoomStatus.free)
    preview = models.ImageField(upload_to='previews/')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Номера'
        verbose_name_plural = 'Номер'


class RoomImages(models.Model):
    image = models.ImageField(upload_to='rooms/')
    post = models.ForeignKey(Room, related_name='images', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        return super(RoomImages, self).save(*args, **kwargs)


