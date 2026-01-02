from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class ConnectionRequest(models.Model):
    sender = models.ForeignKey(
        User,
        related_name="sent_requests",
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        User,
        related_name="received_requests",
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=[("pending", "Pending"), ("accepted", "Accepted")],
        default="pending"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("sender", "receiver")


class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("follower", "following")
