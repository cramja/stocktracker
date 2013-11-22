from django.db import models
from django.contrib.auth.models import User

class Stock(models.Model):
    name = models.CharField(max_length=20, primary_key=True)

class UserStockMapping(models.Model):
    user = models.ForeignKey(User)
    stock = models.ForeignKey(Stock)
