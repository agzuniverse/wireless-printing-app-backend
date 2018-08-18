from django.db import models
from django.contrib.auth.models import User


class Test(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()


class UserData(models.Model):
    id = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    credits = models.IntegerField(default=0)

    def __str__(self):
        return self.id.username

    class Meta:
        verbose_name_plural = "UserData"
