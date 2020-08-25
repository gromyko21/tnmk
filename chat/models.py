from django.db import models
from django.contrib.auth.models import User

class userComment(models.Model):
    sender = models.ForeignKey(User, related_name="sender", on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, blank=True, null=True, related_name="recipient", on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=255, null=True)
