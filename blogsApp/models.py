from django.db import models
from django.conf import settings

class PostGaming(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='postgaming_images/', blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.user.full_name}"


class LikeGaming(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(PostGaming, related_name="likes", on_delete=models.CASCADE)  # 🔥 Ajout du `related_name`
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Un utilisateur ne peut liker un post qu'une seule fois

    def __str__(self):
        return f"{self.user.full_name} a liké {self.post.title}"
