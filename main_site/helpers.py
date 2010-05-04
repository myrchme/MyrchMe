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


def upload_products(filepath,vendor):
    import csv
    reader = csv.reader(open(filepath, 'rU'), dialect='excel-tab')
    products_added = 0
    failed_lines = []
    row_num = 0
    for line in reader:
        if row_num==0:
            header = line
        else:
            def add_optional_field(field):
                return line[header.index(field)] if field in header else None

            #delete any existing product with current prod_id, keeps prod_id
            #unique for each vendor (remember, these are their IDs, not ours)
            models.Product.objects.filter(vendor=vendor,
                                   prod_id=line[header.index("prod_id")]
                                  ).delete()
            #try getting the Category object associated with this line, skip to
            #the next iteration/line if we can't find the category
            try:
                category = models.Category.objects.get(full_title=
                                                line[header.index("category")])
            except ObjectDoesNotExist:
                failed_lines.append(line)
                continue
            try:
                product, created = models.Product.objects.get_or_create(
                    #required fields
                    vendor = vendor,
                    category = category,
                    is_active = True,
                    title = line[header.index("title")],
                    description = line[header.index("description")],
                    prod_id = line[header.index("prod_id")],
                    condition = line[header.index("condition")],
                    price = line[header.index("price")],
                    link = line[header.index("link")],
                    image_url = line[header.index("image_url")],
                    #optional fields
                    isbn = add_optional_field("isbn"),
                    upc = add_optional_field("upc"),
                    brand = add_optional_field("brand"),
                    color = add_optional_field("color"),
                    size = add_optional_field("size"),
                    gender = add_optional_field("gender")
                )
            except:
                failed_lines.append(line)
                continue

            if(created):
                products_added += 1
            else:
                failed_lines.append(line)
        row_num += 1

    return products_added, failed_lines


def save_file(f, folderpath=settings.UPLOAD_DIR, append=""):
    """
    save_file:
    When given a file in memory and a directory path, this writes the file to
    the directory and returns its filepath.
    """
    filepath = folderpath + append + "_" + f.name
    destination = open(filepath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filepath


def generate_key(len=16, key=''):
    """
    generate_key: Used to generate 16 character API keys for vendors.
    """
    chars = string.letters + string.digits
    for i in range(len):
        key = key + choice(chars)
    return key