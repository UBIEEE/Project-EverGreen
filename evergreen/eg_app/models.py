import uuid

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.TextField(blank=False)
    image = models.ImageField(upload_to="image_upload", blank=True, null=True)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    userLikes = models.ManyToManyField(User, blank=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user}: {self.caption}"

    def get_likers_display(self):

        likers = self.userLikes.all()



        number_of_likes = likers.count()


        if number_of_likes == 0:
            return "No likes yet"

        elif number_of_likes <= 3:

            usernames = []
            for user in likers:
                usernames.append(user.username)

            # join the usernames w/ commas
            names_string = ", ".join(usernames)
            return "Liked by: " + names_string


        else:
            # get first 3 USERS
            first_three_users = likers[:3]


            usernames = []
            for user in first_three_users:
                usernames.append(user.username)

            # get how many people liked it other THAN THE 3
            remaining_likes = number_of_likes - 3

            # concat!!!
            names_string = ", ".join(usernames)
            return "Liked by: " + names_string + " and " + str(remaining_likes) + " others"


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.comment}"
