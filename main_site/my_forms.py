"""
my_forms.py
Handles our forms.
"""
from django.shortcuts import render_to_response
from django.contrib.auth import login, authenticate
from string import capitalize
from django import forms
from myrchme.main_site.models import *
from myrchme.main_site.helpers import *
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
    LoginForm:
    """
    username = forms.CharField(label=('Username:'), max_length=100)
    password = forms.CharField(label=('Password:'), widget=forms.PasswordInput)

    def process(self, request):
        error=""
        #if from is fill out, authenticate the user and log them in
        if self.is_valid():
            user = authenticate(username=self.cleaned_data["username"],
                                password=self.cleaned_data["password"])
            if user is not None:
                login(request, user)
                return redirect_logged_in_users(user)
            else:
                error = "Incorrect username and password."
        else:
            error = "Please enter your username and password."
        index_dict = {'login_form':self, 'error':error}
        
        return render_to_response('base/index.html', index_dict)


class RegisterForm(forms.ModelForm):
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
    """
    RegisterPersonForm:
    """
    class Meta:
        model = Person
        fields=('first_name','last_name','gender','username','email_primary')

    def save_person(self):
        user = self.save_user()

        #create and save Person
        person = Person(user = user, email_primary = user.email,
                        username = user.username,
                        first_name=capitalize(self.cleaned_data["first_name"]),
                        last_name = capitalize(self.cleaned_data["last_name"]),
                        gender = self.cleaned_data["gender"])
        person.save()


class RegisterVendorForm(RegisterForm):
    """
    RegisterVendorForm:
    """
    class Meta:
        model = Vendor
        fields= ('company_name','rep_first_name','rep_last_name','username',
                 'email_primary','website_url','buy_url')

    def save_vendor(self):
        #create and save User
        user = self.save_user()

        #create and save Vendor
        vendor = Vendor(user = user, email_primary = user.email,
                username = user.username,
                company_name = capitalize(self.cleaned_data["company_name"]),
                rep_first_name= capitalize(self.cleaned_data["rep_first_name"]),
                rep_last_name = capitalize(self.cleaned_data["rep_last_name"]),
                website_url = self.cleaned_data["website_url"],
                buy_url = self.cleaned_data["buy_url"])
        vendor.save()


class AccountForm(forms.ModelForm):
    """
    AccountForm:
    """
    class Meta:
        model = Person
        exclude = ('user','username','join_date','last_login','is_active',
                   'is_email_subscription'
        )

    def update_account(self, user):
        # save updated Person
        person = get_object_or_404(Person, user=user)
        person.first_name = capitalize(self.cleaned_data["first_name"])
        person.last_name = capitalize(self.cleaned_data["last_name"])
        person.gender = self.cleaned_data["gender"]
        person.email_primary = self.cleaned_data["email_primary"]
        person.gift_freq = self.cleaned_data["gift_freq"]
        person.max_gift_price = self.cleaned_data["max_gift_price"]
        person.min_gift_price = self.cleaned_data["min_gift_price"]
        person.save()


class UploadFileForm(forms.Form):
    file  = forms.FileField()
