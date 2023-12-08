from django.db import models
from django.contrib.auth.models import User

class Game(models.Model):
    name = models.CharField(max_length=127, unique=True)
    icon = models.ImageField(upload_to = 'core/static/game_icons/', null=True, blank=True)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to = 'core/static/user_avatars/', null=True, blank=True)
    games = models.ManyToManyField(Game)
    description = models.TextField()

    def __str__(self):
        return self.user.username

class Collision(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collisions_as_user')
    viewed_user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='collisions_as_viewed_user')
    accepted = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'viewed_user')


