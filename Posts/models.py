from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class Post(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )
    content = models.TextField()
    image = models.ImageField(
        upload_to="posts/images/",
        blank=True,
        null=True
    )
    video = models.FileField(
        upload_to="posts/videos/",
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comments.filter(parent__isnull=True).count()

    def __str__(self):
        return f"Post by {self.author}"



class Like(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    class Meta:
        unique_together = ("user", "post")

    def __str__(self):
        return f"{self.user} likes {self.post}"



class Comment(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()

    # 🔥 This enables nested comments / replies
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def is_reply(self):
        return self.parent is not None

    def __str__(self):
        return f"Comment by {self.user}"


from django.db import models

class News(models.Model):
    title = models.CharField(max_length=200)
    tag = models.CharField(max_length=50)   # django, python, ai, jobs
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title
