from myrchme.main_site.models import *
from myrchme.main_site.my_forms import *
from myrchme.main_site.helpers import *
from django.forms.models import inlineformset_factory
#HTTP rendering tools
from django.shortcuts import render_to_response, get_object_or_404, redirect
#Django Authentication stuff
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import SetPasswordForm


def index(request):
    """
    index:
    Main page logic.
    """
    if request.user.id:
        return redirect('/profile')
    login_form = LoginForm()
    return render_to_response('base/index.html', 
                             {'login_form':login_form})


def register_person(request):
    """
    register_person:
    """
    if request.user.id:
        return redirect('/profile')

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
                form.error = "Form error."

    else:
        #request is a GET (seeing page for 1st time)
        form = RegisterPersonForm()
        
    return render_to_response('base/register.html', {'form':form})


def register_vendor(request):
    """
    register_vendor:
    """
    if request.user.id:
        return redirect('/store-profile')

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
                form.error = "Form error."

    else:
        #request is a GET (seeing page for 1st time)
        form = RegisterVendorForm()

    return render_to_response('base/register-vendor.html', {'form':form})


@login_required
def change_person_account(request):
    """
    change_person_account:
    """
    curr_person = Person.objects.get(username=request.user.username)
    curr_first_name = curr_person.first_name
    curr_last_name = curr_person.last_name
    curr_email_primary = curr_person.email_primary
    curr_email_subcription = curr_person.email_subscription
    curr_shipping_address = curr_person.shipping_address

    return render_to_response('base/account.html', )


@login_required
def view_person_profile(request):
    """
    view_person_profile:
    """
    curr_person = Person.objects.get(username=request.user.username)
    preferences = PersPref.objects.filter(user=curr_person)
    transactions = Transactions.objects.filter(buyer=curr_person)

    return render_to_response('base/profile.html', {'person':curr_person,
                                                'preferences':preferences,
                                                'transactions':transactions})

@login_required
def view_store_profile(request):
    """
    view_store_profile:
    """
    curr_vendor = Vendor.objects.get(username=request.user.username)
    transactions = Transactions.objects.filter(vendor=curr_vendor)

    return render_to_response('base/profile.html', {'vendor':curr_vendor,
                                                'transactions':transactions})

@login_required
def view_public_store_profile(request):
    """
    view_public_store_profile
    """
    curr_vendor = Vendor.objects.get(username=store)

    # displays top ten rated items
    curr_top_items = Vender.objects.filter(
        vendor=curr_vendor).filter(isActive=True).order_by('-rating')[:10]

    return render_to_response('base/storefront.html',
                              {'vendor':curr_vendor,
                              'top items':curr_top_items})


@user_login_required
def set_preferences(request):
    """
    set_preferences
    """
    curr_user = request.user
    curr_person = Person.objects.get(username=curr_user.username)
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


def upload_products(file,vendor):
    products_added = 0;
    failed_products = []
    import csv
    reader = csv.reader(open(file, 'rU'), dialect='excel-tab')
    for line in reader:
        new_product, created = Product.objects.get_or_create(
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
            failed_products.append(new_product)
    return products_added, failed_products
