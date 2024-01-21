from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Users(models.Model):
    user = models.OneToOneField(User, related_name="account", on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'users'
    def __str__(self):
        return self.user.first_name