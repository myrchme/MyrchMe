"""
helpers.py
A collection of general helper functions.
"""
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import user_passes_test
from myrchme.main_site.models import *
from django.contrib.auth import REDIRECT_FIELD_NAME
from random import choice
import string

def user_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME,
                        user_type='User'):
    """
    Decorator for views that checks that a Person is logged in, redirecting
    to the log-in page if necessary.
    """
    if user_type=='Person':
        actual_decorator = user_passes_test(
            lambda u: (u.is_authenticated() and u.is_active()) and
                      (Person.objects.filter(username=u.username).count()==1),
            redirect_field_name=redirect_field_name
        )
    elif user_type=='Vendor':
        actual_decorator = user_passes_test(
            lambda u: (u.is_authenticated() and u.is_active()) and
                      (Vendor.objects.filter(username=u.username).count()==1),
            redirect_field_name=redirect_field_name
        )
    else:
        actual_decorator = user_passes_test(
            lambda u: (u.is_authenticated() and u.is_active()),
            redirect_field_name=redirect_field_name
        )
    if function:
        return actual_decorator(function)

    return actual_decorator


def vendor_login_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that a Vendor is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (u.is_authenticated() and u.is_active()) and
                  (Vendor.objects.filter(username=u.username).count()==1),
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


def logout_user(request, send_to='/'):
    """
    logout_user:
    Logs out user, redirects to send_to.
    """
    logout(request)
    return redirect(send_to)


def generate_key(len=16, key=''):
    chars = string.letters + string.digits
    for i in range(len):
        key = key + choice(chars)
    return key