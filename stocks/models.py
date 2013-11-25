from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    code = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    recommended = models.BooleanField()

class UserProfile(models.Model):
    user = models.ForeignKey(User, primary_key=True, unique=True)
    interests = models.ManyToManyField(Stock)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
