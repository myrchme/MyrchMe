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
    last_login = models.DateTimeField(auto_now=True)

    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    GENDER = (('M', 'Male'),('F', 'Female'))
    gender = models.CharField(max_length=1, choices=GENDER)
    email_primary = models.EmailField(unique=True)
    email_subscription = models.BooleanField(default=True)

    #Location Information
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5, blank=True)
    state = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)

    #Payment info (needs to be secured later)
    cc_number = models.PositiveIntegerField(max_length=16, blank=True)
    card_sec_code = models.PositiveIntegerField(max_length=3, blank=True)

    #Global gift preferences
    FREQ_CHOICES = (
        ('WEEK', 'Weekly'),
        ('BIWK', 'Bi-weekly'),
        ('MNTH', 'Monthly'),
        ('OFF', 'Off')
    )
    gift_freq = models.CharField(max_length=4, default='OFF')
    max_gift_price = models.PositiveIntegerField(max_length=9)
    min_gift_price = models.PositiveIntegerField(max_length=9, blank=True,
                                                 default=0)

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
    phone = models.PositiveIntegerField(max_length=14, blank=True)
    
    join_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    rep_first_name = models.CharField(max_length=40)
    rep_last_name = models.CharField(max_length=40)
    rep_email_primary = models.EmailField(unique=True)

    # Directs us to the vendor's implementation of the Buy API
    buy_url = models.URLField(max_length=300)

    def __unicode__(self):
        return '%s \n %s \n %s %s \n Join Date:%s' % (self.vendor_username,
            "-"*20, self.rep_first_name, self.rep_last_name, self.join_date)

class Category(models.Model):
    """
    Category:
    Represents product categories.
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500, blank=True)
    parent = models.ForeignKey('self', null=True, default=None)

    def __unicode__(self):
        return '%s \n %s \n %s' % (self.title,"-"*20, self.description)

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
    brand = models.CharField(max_length=50, blank=True)
    isbn = models.PositiveIntegerField(max_length=13, blank=True)
    category = models.ForeignKey(Category)
    upc = models.CharField(max_length=12, blank=True)
    color = models.CharField(max_length=20, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES ,blank=True)

    create_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s \n %s \n %s %s \n Create Date:%s' % (self.title,
            "-"*20, self.vendor, self.prod_id, self.create_date)


class PersPref(models.Model):
    """
    PersPref:
    Stores a users preferences to generate item choice.
    """
    user = models.ForeignKey(Person)
    category = models.ForeignKey(Category)
    tagwords = models.CharField(max_length=500, blank=True)
    history = models.CharField(max_length=500, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, blank=True)


class Transaction(models.Model):
    """
    Transaction:
    Stores data associated with each transaction.
    """
    buyer = models.ForeignKey(Person)
    item = models.ForeignKey(Product)
    create_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    STATUS_CHOICES = (
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    details = models.CharField(max_length=500, blank=True)


class ProductVote(models.Model):
    """
    ProductVote:
    Stores user's votes on products
    """
    user = models.ForeignKey(Person)
    product = models.ForeignKey(Product)
    date = models.DateTimeField(auto_now_add=True)
    #an integer from 1 to 5
    vote = models.PositiveIntegerField(max_length=1)

class ProductComment(models.Model):
    """
    ProductComment:
    Stores user's comments on products.
    """
    user = models.ForeignKey(Person)
    product = models.ForeignKey(Product)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()