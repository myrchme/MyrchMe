"""
helpers.py
A collection of general helper functions.
"""
#setup Django environment first
from django.core.management import setup_environ
from myrchme import settings
setup_environ(settings)

import string
import models
from django.shortcuts import redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from random import choice



def is_person(user):
    return models.Person.objects.filter(username=user.username).count()==1

def is_vendor(user):
    return models.Vendor.objects.filter(username=user.username).count()==1

def redirect_logged_in_users(user):
    """
    redirect_logged_in_users:
    Redirects logged in users away from pages they shouldn't see.
    E.g. Registration pages.
    """
    if models.Person.objects.filter(username=user.username).count()==1:
        return redirect('/user/'+user.username)
    elif models.Vendor.objects.filter(username=user.username).count()==1:
        return redirect('/store-profile')
    else:
        return redirect('/logout') #logs out admin users


def user_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                        user_type='User'):
    """
    user_login_required:
    Decorator for views that checks that if a certain type of User is logged in,
    redirecting to the log-in page if not.
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
    login_user: Authenticates the user, logins them in, redirects to send_to.
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
    """
    generate_key: Used to generate 16 character API keys for vendors.
    """
    chars = string.letters + string.digits
    for i in range(len):
        key = key + choice(chars)
    return key