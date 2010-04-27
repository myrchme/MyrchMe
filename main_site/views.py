from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.forms.models import inlineformset_factory
from myrchme.main_site.models import *
from myrchme.main_site.my_forms import *
from myrchme.main_site.helpers import *
from cgi import escape
#HTTP rendering tools
#Django Authentication stuff
#from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import SetPasswordForm


def index(request):
    """
    index:
    Main page logic.
    """
    if request.user.id:
        return redirect_logged_in_users(request.user)
    error = ""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        return form.process(request)
            
    login_form = LoginForm()
    index_dict = {'login_form':login_form, 'error':error}
    return render_to_response('base/index.html', index_dict)


def register_person(request):
    """
    register_person:
    Serves registration page for Persons and registers them.
    """
    redirect_logged_in_users(request.user)

    #handles registration form, registers user
    if request.method == 'POST':
        form = RegisterPersonForm(request.POST)
        #if from is valid, add the user and log them in
        if form.is_valid():
            form.save_person()
            user = authenticate(username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            login(request, user)
            return redirect('/profile')
        else:
            form.error = "Form not valid."

    else:
        #request is a GET (seeing page for 1st time)
        form = RegisterPersonForm()
        
    return render_to_response('base/register.html', {'form':form})


def register_vendor(request):
    """
    register_vendor:
    Serves registration page for Vendors and registers them.
    """
    if request.user.id:
        return redirect_logged_in_users(request.user)

    #handles registration form, registers user
    if request.method == 'POST':
        form = RegisterVendorForm(request.POST)
        #if from is valid, add the user and log them in
        if form.is_valid():
                form.save_vendor()
                user = authenticate(username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password"])
                login(request, user)
                return redirect('/store-profile')
        else:
                form.error = "Form not valid."

    else:
        #request is a GET (seeing page for 1st time)
        form = RegisterVendorForm()

    return render_to_response('base/register_vendor.html', {'form':form})


@user_login_required(user_type='Person')
def change_person_account(request):
    """
    change_person_account:
    """
    curr_person = get_object_or_404(Person, user=request.user)
    account_dict= { 'first_name':curr_person.first_name,
                    'last_name':curr_person.last_name,
                    'email':curr_person.email_primary,
                    'is_subscribed':curr_person.is_email_subscription,
                    'shipping_address':curr_person.shipping_address,
                    'user':request.user
    }
    return render_to_response('base/account.html', account_dict)


def view_person_profile(request, username): #request MUST be an arg here or
                                            #function fails
    """
    view_person_profile:
    """
    curr_person = get_object_or_404(Person, username=escape(username))
    preferences = PersPref.objects.filter(user=curr_person)
    transactions = Transaction.objects.filter(buyer=curr_person)
    profile_dict= { 'person':curr_person,
                    'preferences':preferences,
                    'transactions':transactions,
                    'user':request.user
    }
    return render_to_response('base/profile.html', profile_dict)


@user_login_required(user_type='Vendor')
def view_my_store_profile(request):
    """
    view_store_profile:
    """
    curr_vendor = get_object_or_404(Vendor, user=request.user)
    transactions = Transaction.objects.filter(vendor=curr_vendor)
    profile_dict = {'vendor':curr_vendor,
                    'transactions':transactions,
                    'user': request.user
    }
    
    return render_to_response('base/store_profile.html', profile_dict)


def view_store(request, username):
    """
    view_store
    """
    curr_vendor = get_object_or_404(Vendor, username=escape(username))

    # displays top ten rated items
    curr_top_items = Product.objects.filter(vendor=curr_vendor
                     ).filter(is_active=True
                     ).order_by('-avg_rating')[:10]
    profile_dict = {'vendor':curr_vendor,
                    'top_items':curr_top_items,
                    'user': request.user
    }

    return render_to_response('base/storefront.html', profile_dict)


@user_login_required(user_type='Person')
def set_preferences(request):
    """
    set_preferences
    """
    curr_person = get_object_or_404(Person, user=request.user)
    preferences = PersPref.objects.filter(user=curr_person)

    PersPrefFormSet = inlineformset_factory(Person, PersPref, max_num=1)
    pref_form = PersPrefFormSet(instance=curr_person)
    
    if request.method == 'POST':
        pref_form = PersPrefFormSet(request.POST, instance=curr_person)
        if pref_form.is_valid():
            pref_form.save()
            message = "Preferences successfully saved."
            return render_to_response('base/preferences.html',
                {'preferences':preferences, 'pref_form':pref_form,
                 'message':message})
        else:
            pref_form.error = pref_form.errors
            
    return render_to_response('base/preferences.html',
                             {'preferences':preferences,
                              'pref_form':pref_form, 'errors':pref_form.errors})


def logout_view(request):
    logout(request)
    return redirect('/')


@user_login_required(user_type='Person')
def buy_view(request, id):
    return redirect('/')


def upload_products(file,vendor):
    products_added = 0;
    failed_products = []
    import csv
    reader = csv.reader(open(file, 'rU'), dialect='excel-tab')
    for line in reader:
        product, created = Product.objects.get_or_create(
            vendor = vendor,
            prod_id = line[0],
            category = line[1],
            title = line[2],
            condition = line[3],
            description = line[4],
            price = line[5],
            link = line[6],
            image_url = line[7],
            isbn = line[8],
            upc = line[9],
            brand = line[10],
            color = line[11],
            size = line[12])
        if(created):
            products_added += 1
        else:
            failed_products.append(product)
    return products_added, failed_products
