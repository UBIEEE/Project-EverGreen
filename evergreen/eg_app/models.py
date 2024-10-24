from django.db import models

# Create your models here.

class Account(models.Model):
    email = models.EmailField(unique=True)
    pwdHash = models.BinaryField()


class AuthToken(models.Model):
    token = models.TextField()
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
