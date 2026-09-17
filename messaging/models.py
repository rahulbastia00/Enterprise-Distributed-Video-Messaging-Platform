from django.db import models
from django.contrib.auth.models import User

class Channel(models.Model):
    name = models.CharField(max_length=80, unique=True)
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="channels")

    def __str__(self):
        return self.name

class Message(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-timestamp']