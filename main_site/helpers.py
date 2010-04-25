"""
helpers.py
A collection of general helper functions.
"""
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from random import choice
import string


def is_person(user):
    from myrchme.main_site.models import Person #only works when placed here???
    return Person.objects.filter(username=user.username).count()==1

def is_vendor(user):
    from myrchme.main_site.models import Vendor
    return Vendor.objects.filter(username=user.username).count()==1

def redirect_logged_in_users(user):
    """
    redirect_logged_in_users:
    Redirects logged in users away from pages they shouldn't see.
    E.g. Registration pages.
    """
    from myrchme.main_site.models import Person, Vendor
    if Person.objects.filter(username=user.username).count()==1:
        return redirect('/profile')
    elif Vendor.objects.filter(username=user.username).count()==1:
        return redirect('/store-profile')
    else:
        return redirect('/youcannevergethere')


def user_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                        user_type='User'):
    """
    Decorator for views that checks that a Person is logged in, redirecting
    to the log-in page if necessary.
    """
    if user_type=='Person':
        actual_decorator = user_passes_test(
            lambda u: is_person(u),
            redirect_field_name=redirect_field_name
        )
    elif user_type=='Vendor':
        actual_decorator = user_passes_test(
            lambda u: is_vendor(u),
            redirect_field_name=redirect_field_name
        )
    else:
        actual_decorator = user_passes_test(
            lambda u: u.is_authenticated() and u.is_active(),
            redirect_field_name=redirect_field_name
        )
    if function:
        return actual_decorator(function)

    return actual_decorator


def login_user(request, send_to='/profile.html'):
    """
    login_user:
    Authenticates the user, logins them in, redirects to send_to.
    """
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return redirect(send_to)
        else:
            error="Disabled account."
    else:
        error="Incorrect username or password."
    return error


def generate_key(len=16, key=''):
    chars = string.letters + string.digits
    for i in range(len):
        key = key + choice(chars)
    return key