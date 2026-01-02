# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.db import models
class User(AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('professional', 'Professional'),
        ('recruiter', 'Recruiter'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    headline = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    company = models.CharField(max_length=150, blank=True)
    college = models.CharField(max_length=150, blank=True)

    profile_image = models.ImageField(
        upload_to="profiles/",
        blank=True,
        null=True
    )

    # ✅ ADD THIS
    skills = models.CharField(
        max_length=500,
        blank=True,
        help_text="Comma separated skills (e.g. Python, Django, React)"
    )

    def __str__(self):
        return f"{self.user.username}'s Profile"


from django.db.models.signals import post_save
from django.dispatch import receiver