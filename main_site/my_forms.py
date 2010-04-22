"""
my_forms.py
Handles our forms.
"""

from django.forms import ModelForm
from django import forms
from django.db import models
from myrchme.main_site.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import *



class RegisterForm(ModelForm):
    """
    RegisterForm:
    Form generated for registering users.
    """
    password = forms.CharField(label=('password'), widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields=('first_name','last_name','gender','username','email_primary')

    def clean_username(self):
        """
        Sanitize input for username
        """

        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError("A user with that username already exists.")

    def clean_email(self):
        """
        Sanitize email
        """
        email_primary = self.cleaned_data["email_primary"]

        try:
            Person.objects.get(email_primary=email_primary)
        except Person.DoesNotExist:
            return email_primary
        raise forms.ValidationError("Email address already exists.")

    def clean_password(self):
        """
        Sanitize input for password. Check if two passwords are equal.
        Check password length.
        """

        password = self.cleaned_data['password']
        #password2 = self.cleaned_data['password2']

       # if (password != self.password2):
            #raise forms.ValidationError("Your two passwords don't match.")
        if len(password) < 6:
            raise forms.ValidationError("Your password must be at least" +
                                        "6 characters long.")
        return password

    def save(self, request, commit=True):

        #get registration info and clean
        username = self.clean_username()
        password = self.clean_password()
        email = self.clean_email()

        #save username
        new_user = User.objects.create(username=username)
        new_user.save()

        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()

        #new lines necessary to create Person object when creating a User
        person = Person(user=user, email_primary=email, username=username,
                        first_name=self.cleaned_data["first_name"],
                        last_name=self.cleaned_data["last_name"],
                        gender=self.cleaned_data["gender"])
        person.save()

        #login in the user
        user = authenticate(username=username, password=password)
        login(request, user)
        self.instance.user_id = user.id
        return user

