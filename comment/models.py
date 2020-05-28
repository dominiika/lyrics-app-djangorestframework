from django.db import models
from django.contrib.auth import get_user_model
from song.models import Song


class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    content = models.TextField()

    created_at_time = models.DateTimeField(auto_now_add=True,)
    edited = models.BooleanField(default=False)
    edited_at_time = models.DateTimeField(auto_now=True)

    def no_of_likes(self):
        number_of_likes = self.likes.count()
        return number_of_likes

    def __str__(self):
        if len(self.content) > 50:
            name = self.content[:50] + "..."
        else:
            name = self.content
        return name


class CommentLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        unique_together = (("user", "comment"),)
        index_together = (("user", "comment"),)

    def __str__(self):
        name = "{0.user} - {0.comment}"
        return name.format(self)
