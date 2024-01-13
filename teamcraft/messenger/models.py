import uuid

from django.utils import timezone

from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ChatRoom(models.Model):
    roomId = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(User)

    def __str__(self):
        return f'Room {self.roomId}'


class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='msg_receiver')
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self}'

    def delete_message(self):
        self.delete()

