from django.db import models
from django.contrib.auth.models import User
#from django.contrib import admin

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
    cc_number = models.IntegerField(max_length=16, blank=True)
    card_sec_code = models.IntegerField(max_length=3, blank=True)
    
    FREQ_CHOICES = (
        ('WEEK', 'Extra-small'),
        ('BIWK', 'Small'),
        ('MNTH', 'Medium'),
        ('OFF', 'Large')
    )
    gift_freq = models.CharField(max_length=4, default='OFF')

    def __unicode__(self):
            return '%s \n %s \n %s %s \n Join Date:%s' % (self.username, "-" *
        20, self.first_name, self.last_name, self.join_date)


class Vendor(models.Model):
    """
    Vendor:
    Holds data related to our vendor's accounts.
    """
    vendor = models.ForeignKey(User, unique=True)
    vendor_username = models.CharField(max_length=40, unique=True)
    company_name = models.CharField(max_length=40)
    website_URL = models.URLField(max_length=300, verify_exists=True)
    join_date = models.DateTimeField(auto_now_add=True)

    rep_first_name = models.CharField(max_length=40)
    rep_last_name = models.CharField(max_length=40)
    rep_email_primary = models.EmailField(unique=True)

    # Directs us to the vendor's implementation of the Buy API
    buy_url = models.URLField(max_length=300)


class Category(models.Model):
    """
    Category:
    Represents product categories.
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)


class Subcategory(models.Model):
    """
    Subcategory:
    Represents product subcategories.
    """
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)


SIZE_CHOICES = (
        ('XS', 'Extra-small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra-Large'),
        ('XXL', 'Double Extra-Large')
    )


class Product(models.Model):
    """
    Product:
    Stores data relevant to products, provided by our partners.
    """
    vendor = models.ForeignKey(Vendor)
    title = models.CharField(max_length=70)
    description = models.TextField()
    prod_id = models.CharField(max_length=30)
    CONDITION_CHOICES = (
        ('NEW', 'New'),
        ('USED', 'Used'),
        ('REFURB', 'Refurbished')
    )
    condition = models.CharField(max_length=6, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    link = models.URLField(verify_exists=True, max_length=300)
    #image = models.ImageField(upload_to=None)
    image_url = models.URLField(verify_exists=True, max_length=300)
    brand = models.CharField(max_length=50)
    isbn = models.IntegerField(max_length=13, blank=True)
    category = models.ForeignKey(Category)
    subcategory = category = models.ForeignKey(Subcategory)
    upc = models.CharField(max_length=12, blank=True)
    color = models.CharField(max_length=20, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES ,blank=True)


class PersPref(models.Model):
    """
    PersPref:
    Stores a users preferences to generate item choice.
    """
    user = models.ForeignKey(Person)
    category = models.ForeignKey(Category)
    subcategory = models.ForeignKey(Subcategory)
    tagwords = models.CharField(max_length=500)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, blank=True)


class Transaction(models.Model):
    """
    Transaction:
    Stores data associated with each transaction.

    """
    buyer = models.ForeignKey(Person)
    item = models.ForeignKey(Product)
    vendor = models.ForeignKey(Vendor)
    date = models.DateTimeField(auto_now_add=True)
    STATUS_CHOICES = (
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'delivered')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    details = models.CharField(max_length=500)