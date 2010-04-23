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
    curr_user = request.user
    return render_to_response('base/index.html', {'curr_user':curr_user})


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
def view_person_profile(request):
    """
    view_person_profile:
    """
    return render_to_response('base/profile.html')


@login_required
def view_store_profile(request):
    """
    view_store_profile:
    """
    return render_to_response('base/store_profile.html')


@login_required
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
