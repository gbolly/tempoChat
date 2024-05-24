from django.db import models
from django.contrib.auth.models import User


class Conversation(models.Model):
    id = models.AutoField(primary_key=True)
    participants = models.ManyToManyField(User, related_name="conversations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        participants_usernames = ' and '.join(
            participant.username for participant in self.participants.all())
        return f"Conversation between {participants_usernames}"
