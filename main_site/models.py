from django.db import models
from django.contrib.localflavor.us.models import USStateField
from django.contrib.auth.models import User
from myrchme.main_site.helpers import generate_key
#from django.contrib import admin


GENDER = (('M', 'Male'),('F', 'Female'))

class Person(models.Model):
    """
    Person:
    Stores user data. We are extending Django's built in User and Auth models.
    """
    user = models.ForeignKey(User, unique=True)
    username = models.CharField(max_length=40, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER)
    email_primary = models.EmailField(unique=True)
    is_email_subscription = models.BooleanField(default=True)
    shipping_address = models.ForeignKey('PhysicalAddress',blank=True,null=True)
    credit_card = models.ForeignKey('CreditCard', blank=True, null=True)
   
    #Global gift preferences
    FREQ_CHOICES = (
        ('WEEK', 'Weekly'),
        ('BIWK', 'Bi-weekly'),
        ('MNTH', 'Monthly'),
        ('OFF', 'Off')
    )
    gift_freq = models.CharField(max_length=4, choices=FREQ_CHOICES,
                                 default='OFF')
    max_gift_price = models.PositiveIntegerField(max_length=9, default=100)
    min_gift_price = models.PositiveIntegerField(max_length=9, default=0)

    #To be added: privacy options

    def __unicode__(self):
            return self.username


class Vendor(models.Model):
    """
    Vendor:
    Holds data related to our vendor's accounts.
    """
    user = models.ForeignKey(User, unique=True)
    username = models.CharField(max_length=40, unique=True)
    company_name = models.CharField(max_length=40)
    website_url = models.URLField(max_length=300, verify_exists=True)
    phone = models.PositiveIntegerField(max_length=14, null=True, blank=True)
    
    join_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    rep_first_name = models.CharField(max_length=40)
    rep_last_name = models.CharField(max_length=40)
    email_primary = models.EmailField(unique=True)

    #Directs us to the vendor's implementation of the Buy API
    buy_url = models.URLField(max_length=300, verify_exists=False)
    #API key used for API authentication
    api_key = models.CharField(default=generate_key(),max_length=20,unique=True)

    def __unicode__(self):
        return self.username


class Category(models.Model):
    """
    Category:
    Represents product categories.
    """
    title = models.CharField(max_length=100)
    full_title = models.CharField(max_length=500, unique=True)
    description = models.CharField(max_length=500, blank=True)
    parent = models.ForeignKey('self', null=True, default=None)

    def __unicode__(self):
        return self.full_title


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
    prod_id = models.CharField(max_length=30) #vendor's prod_id, not ours
    category = models.ForeignKey(Category)
    is_active = models.BooleanField(default=True)
    CONDITION_CHOICES = (
        ('NEW', 'New'),
        ('USED', 'Used'),
        ('REFURB', 'Refurbished')
    )
    condition = models.CharField(max_length=6, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    link = models.URLField(verify_exists=True, max_length=300)
    image_url = models.URLField(verify_exists=True, max_length=300)

    # Rating: an integer from 1 to 5
    avg_rating = models.PositiveIntegerField(max_length=1, default=3)

    #optional fields
    brand = models.CharField(max_length=50, blank=True, null=True)
    isbn = models.CharField(max_length=13, blank=True, null=True)
    upc = models.CharField(max_length=12, blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, null=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES , blank=True,
                            null=True)
    gender = models.CharField(max_length=1, choices=GENDER, blank=True,
                              null=True)

    create_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return str(self.id) + " " + self.title


class PersPref(models.Model):
    """
    PersPref: Stores a users preferences to generate item choice.
    """
    user = models.ForeignKey(Person)
    category = models.ForeignKey(Category)
    tagwords = models.CharField(max_length=500, blank=True)
    history = models.CharField(max_length=500, blank=True)
    size = models.CharField(max_length=3, choices=SIZE_CHOICES, blank=True)

    def __unicode__(self):
        return str(self.id) + " " + self.category.full_title


class Transaction(models.Model):
    """
    Transaction:
    Stores data associated with each transaction.
    """
    buyer = models.ForeignKey(Person)
    vendor = models.ForeignKey(Vendor)
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
    
    def __unicode__(self):
        return str(self.id) + " " + self.item.title


class ProductRating(models.Model):
    """
    ProductVote:
    Stores user's votes on products
    """
    user = models.ForeignKey(Person)
    product = models.ForeignKey(Product)
    date = models.DateTimeField(auto_now_add=True)
    #an integer from 1 to 5
    rating = models.PositiveIntegerField(max_length=1)


class ProductComment(models.Model):
    """
    ProductComment:
    Stores user's comments on products.
    """
    user = models.ForeignKey(Person)
    product = models.ForeignKey(Product)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()


class PhysicalAddress(models.Model):
    """
    PhysicalAddress:
    Stores physical addresses, used to make shipping and billing addresses.
    """
    street_line1 = models.CharField(max_length=200)
    street_line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=50)
    zip = models.CharField(max_length=5, blank=True)
    state = USStateField(blank=True)
    country = models.CharField(max_length=50)


class CreditCard(models.Model):
    """
    CreditCard:
    Stores credit card info.
    """
    name_on_card = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('VISA', 'Visa'),
        ('MAST', 'MasterCard'),
        ('DISC', 'Discover'),
        ('AMEX', 'American Express')

    )
    type = models.CharField(max_length=4, choices=TYPE_CHOICES)
    number = models.PositiveIntegerField(max_length=16)
    security_code = models.PositiveIntegerField(max_length=3)
    expiration_date = models.DateField()
    billing_address = models.ForeignKey('PhysicalAddress', null=True)