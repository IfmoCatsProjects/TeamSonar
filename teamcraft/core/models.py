from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL


class Game(models.Model):
    name = models.CharField(max_length=128, unique=True)
    icon = models.ImageField(upload_to='', null=True, blank=True)

    def __str__(self):
        return self.name


class Gamer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='', null=True, blank=True)
    games = models.ManyToManyField(Game)
    description = models.TextField()

    def __str__(self):
        return self.user.username


class Collision(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collisions_as_user')
    viewed_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collisions_as_viewed_user')
    accept = models.BooleanField()
    match = models.BooleanField()

    class Meta:
        unique_together = ('user', 'viewed_user')


