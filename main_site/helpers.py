"""
helpers.py
A collection of general helper functions.
"""
from django.contrib.auth import login, authenticate, logout
from random import choice
import string

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