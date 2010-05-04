"""
my_forms.py
Handles custom form creation, processing, and saving.
"""
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render_to_response
from django.contrib.auth import login, authenticate
from string import capitalize
from django import forms
from myrchme.main_site.models import *
from myrchme.main_site.helpers import *
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    """
    LoginForm: Login form that validates the user.
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
    RegisterForm: Parent form used for creating Persons and Vendors.
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
    RegisterPersonForm: Form used to create Persons.
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
    RegisterVendorForm: Form used to create Vendors.
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
    AccountForm: Form to handle account creation and updating.
    """
    class Meta:
        model = Person
        exclude = ('user','username','join_date','last_login','is_active',
                   'email_primary')

    def save(self, user):
        # save updated Person
        try:
            person = Person.objects.get(user=user)
        except ObjectDoesNotExist:
            return redirect('/')
        else:
            person.first_name = capitalize(self.cleaned_data["first_name"])
            person.last_name = capitalize(self.cleaned_data["last_name"])
            person.gender = self.cleaned_data["gender"]
            person.gift_freq = self.cleaned_data["gift_freq"]
            person.max_gift_price = self.cleaned_data["max_gift_price"]
            person.min_gift_price = self.cleaned_data["min_gift_price"]
            person.save()


class CreditCardForm(forms.ModelForm):
    """
    CreditCardForm: Form to handle credit card creation and editing.
    """
    class Meta:
        model = CreditCard
        exclude = ('billing_address')

    # update credit card information, create cc is user doesn't have one
    def save(self, user):
        try:
            person = Person.objects.get(user=user)
        except ObjectDoesNotExist:
            return redirect('/')
        cc = person.credit_card
        if cc is None:
            address = PhysicalAddress()
            address = person.shipping_address
            address.save()
            cc = CreditCard(name_on_card=self.cleaned_data["name_on_card"],
                            type = self.cleaned_data["type"],
                            number = self.cleaned_data["number"],
                            security_code = self.cleaned_data["security_code"],
                            expiration_date=self.cleaned_data["expiration_date"],
                            billing_address= address
            )
            cc.save()
            person.credit_card = cc
            person.save()
        else:
            cc.name_on_card = self.cleaned_data["name_on_card"]
            cc.type = self.cleaned_data["type"]
            cc.number = self.cleaned_data["number"]
            cc.security_code = self.cleaned_data["security_code"]
            cc.expiration_date = self.cleaned_data["expiration_date"]
            cc.save()


class AddressForm(forms.ModelForm):
    """
    AddressForm:
    Form to handle account credit card address creation and editing.
    """
    class Meta:
        model = PhysicalAddress

    # update credit card addresses
    def update_cc_address(self, user):
        try:
            person = Person.objects.get(user=user)
        except ObjectDoesNotExist:
            return redirect('/')
        cc_address = person.credit_card.billing_address
        if cc_address is None:
            cc_address = PhysicalAddress(
                street_line1 = self.cleaned_data["street_line1"],
                street_line2 = self.cleaned_data["street_line2"],
                city = self.cleaned_data["city"],
                zip = self.cleaned_data["zip"],
                state = self.cleaned_data["state"],
                country = self.cleaned_data["country"]
            )
            cc_address.save()
            person.credit_card.billing_address = cc_address #this might break?
            person.save()
        else:
            cc_address.street_line1 = self.cleaned_data["street_line1"]
            cc_address.street_line2 = self.cleaned_data["street_line2"]
            cc_address.city = self.cleaned_data["city"]
            cc_address.zip = self.cleaned_data["zip"]
            cc_address.state = self.cleaned_data["state"]
            cc_address.country = self.cleaned_data["country"]
            cc_address.save()

    # update account addresses (shipping addresses)
    def update_acc_address(self, user):
        try:
            person = Person.objects.get(user=user)
        except ObjectDoesNotExist:
            return redirect('/')
        # checks for an address, updates it if found, if not, creates a new one

        address = person.shipping_address
        if address is None:
            address = PhysicalAddress(
                street_line1 = self.cleaned_data["street_line1"],
                street_line2 = self.cleaned_data["street_line2"],
                city = self.cleaned_data["city"],
                zip = self.cleaned_data["zip"],
                state = self.cleaned_data["state"],
                country = self.cleaned_data["country"]
            )
            address.save()
            person.shipping_address = address
            person.save()
        else:
            address.street_line1 = self.cleaned_data["street_line1"]
            address.street_line2 = self.cleaned_data["street_line2"]
            address.city = self.cleaned_data["city"]
            address.zip = self.cleaned_data["zip"]
            address.state = self.cleaned_data["state"]
            address.country = self.cleaned_data["country"]
            address.save()


class PreferenceForm(forms.ModelForm):
    """
    PreferenceForm: Form to handle the creation of new PersPrefs.
    """
    class Meta:
        model = PersPref
        exclude = ('user')

    # adds a PersPref to the DB
    def save(self, user):
        try:
            person = Person.objects.get(user=user)
        except ObjectDoesNotExist:
            return redirect('/')
        else:
            perspref = PersPref(user = person,
                                category = self.cleaned_data["category"],
                                tagwords = self.cleaned_data["tagwords"],
                                history = self.cleaned_data["history"],
                                size = self.cleaned_data["size"]
            )
            perspref.save()


class UploadFileForm(forms.Form):
    """
    UploadFileForm: Form for uploading files (CSV).
    """
    file  = forms.FileField()
