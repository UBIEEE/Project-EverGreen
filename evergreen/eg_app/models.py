from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import uuid

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.TextField(blank=False)

    image = models.ImageField(upload_to="posts",blank=True,null=True)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)



    #list_of_users_who_liked = ArrayField(User,models.CharField(max_length=30))

    #userLikes = models.ManyToManyField(User.username,blank=True)

    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}: {self.caption}"

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.comment}"
