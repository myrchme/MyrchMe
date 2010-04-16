from django.db import models
#from django.contrib import admin
from django.contrib.auth.models import User
#from django.db.models.signals import post_save

class Person(models.Model):
    """
    Person:
    Stores user data. We are extending Django's built in User and Auth models.
    """
    user = models.ForeignKey(User, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)

    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    email_primary = models.EmailField(unique=True)
    email_subscription = models.BooleanField(default=False)

    #Location Information
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)

    #Payment info
    credit = null

    def __unicode__(self):
            return '%s \n %s \n %s %s \n Join Date:%s' % (self.username, "-" *
        20, self.first_name, self.last_name, self.join_date)


class Transaction(models.Model):
    """
    Transaction:

    """

class Product(models.Model):
    """
    Product:

    """
    name =
    description =
    price =
    primary_image =
    primary_category =
    secondary_category =
    subcategory =
    price =
    url =
    #rating = doesn't go here??


class ProductVote(models.Model):
    """
    ProductVote:

    """

