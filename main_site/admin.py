"""
admin.py:
This file dictates what models are configurable from the admin backend.
Go to /admin to view it.
"""

from myrchme.main_site.models import *
from django.contrib import admin

admin.site.register(Person)
admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(PersPref)
admin.site.register(Transaction)