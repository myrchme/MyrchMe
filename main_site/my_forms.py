"""
my_forms.py
Handles our forms.
"""

from django.forms import ModelForm
from django import forms
from django.db import models
from myrchme.main_site.models import *
from django.contrib.auth.models import User
from django.http import *


class RegisterForm(ModelForm):
    """
    RegisterForm:
    Parent form used for creating Persons and Vendors.
    """
    password = forms.CharField(label=('password'), widget=forms.PasswordInput)

    def save_user(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']
        email = self.cleaned_data['email_primary']
        user = User.objects.create_user(username,email,password)
        return user


class RegisterPersonForm(RegisterForm):
    class Meta:
        model = Person
        fields=('first_name','last_name','gender','username','email_primary')

    def save_person(self):
        user = self.save_user()

        #create and save Person
        person = Person(user = user, email_primary = user.email,
                        username = user.username,
                        first_name = self.cleaned_data["first_name"],
                        last_name = self.cleaned_data["last_name"],
                        gender = self.cleaned_data["gender"])
        person.save()


class RegisterVendorForm(RegisterForm):
    class Meta:
        model = Vendor
        fields= ('company_name','rep_first_name','rep_last_name','username',
                 'email_primary','website_URL','buy_URL')

    def save_person(self):
        #create and save User
        user = self.save_user()

        #create and save Person
        vendor = Vendor(user = user, email_primary = user.email,
                        username = user.username,
                        company_name = self.cleaned_data["company_name"],
                        rep_first_name = self.cleaned_data["rep_first_name"],
                        rep_last_name = self.cleaned_data["rep_last_name"],
                        website_URL = self.cleand_date["website_URL"],
                        buy_URL = self.cleaned_data["buy_URL"])
        vendor.save()


