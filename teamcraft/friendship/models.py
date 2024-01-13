from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL


class Friends(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')

    def __str__(self):
        return self.user.username

    def add_friend(self, friend):
        if not friend in self.friends.all():
            self.friends.add(friend)
            self.save()

    def remove_friend(self, friend):
        if friend in self.friends.all():
            self.friends.remove(friend)


class Follow(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_receiver')
    is_active = models.BooleanField(default=True, blank=True, null=False)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.sender.username

    def accept(self):
        receiver_friends = Friends.objects.get(user=self.receiver)
        sender_friends = Friends.objects.get(user=self.sender)

        if receiver_friends:
            receiver_friends.add_friend(self.sender)
            if sender_friends:
                sender_friends.add_friend(self.receiver)
                self.is_active = False
                self.save()

    def decline(self):
        receiver_friends = Friends.objects.get(user=self.receiver)


    def cancel(self):
        self.is_active = False
        self.save()

