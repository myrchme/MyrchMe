from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import logout
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.forms.models import inlineformset_factory
from myrchme.main_site.models import *
from myrchme.main_site.my_forms import *
from myrchme.main_site.helpers import *
from myrchme.settings import UPLOAD_DIR
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
            return redirect('/user/'+user.username)
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
    
    #initialize form fields with curr_person data
    form = AccountForm(instance=curr_person)
    account_dict= {'form':form,'user':request.user}
    return render_to_response('base/user/account.html', account_dict)


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
    return render_to_response('base/user/profile.html', profile_dict)


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
    
    return render_to_response('base/store/store_profile.html', profile_dict)


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

    return render_to_response('base/store/storefront.html', profile_dict)


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

    pref_dict = {'preferences':preferences,
                 'pref_form':pref_form,
                 'errors':pref_form.errors,
                 'user':request.user
    }        
    return render_to_response('base/user/preferences.html', pref_dict)


def logout_view(request):
    logout(request)
    return redirect('/')


@user_login_required(user_type='Person')
def buy_view(request, id):
    #TODO: make a remote buy request
    return redirect('/')


@user_login_required(user_type='Vendor')
def view_inventory(request):
    curr_vendor = get_object_or_404(Vendor, user=request.user)
    products = Product.objects.filter(vendor=curr_vendor)
    invt_dict = {'products':products, 'user':request.user}

    return render_to_response('base/store/inventory.html', invt_dict)


def view_product(request, id):
    product = get_object_or_404(Product, id=id)
    prod_dict = {'product':product, 'user':request.user}
    
    return render_to_response('base/product_details.html', prod_dict)


@user_login_required(user_type='Vendor')
def upload_products_view(request):
    curr_vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
           folderpath = UPLOAD_DIR + "vendor/"
           filepath = save_file(request.FILES['file'], folderpath,
                                request.user.username)
           num_added, failed_lines = upload_products(filepath, curr_vendor)
           results_dict = {'num_added':num_added,
                           'failed_lines':failed_lines,
                           'user':request.user}
           return render_to_response('base/store/upload_results.html', results_dict)
    else:
        form = UploadFileForm()
        form_dict = {'form': form,'user':request.user}
        return render_to_response('base/store/upload.html', form_dict)


def save_file(f, folderpath=UPLOAD_DIR, append=""):
    filepath = folderpath + append + "_" + f.name
    destination = open(filepath, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filepath

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
            Product.objects.filter(vendor=vendor, 
                                   prod_id=line[header.index("prod_id")]
                                  ).delete()
            #try getting the Category object associated with this line, skip to
            #the next iteration/line if we can't find the category
            try:
                category = Category.objects.get(full_title=
                                                line[header.index("category")])
            except ObjectDoesNotExist:
                #raise ObjectDoesNotExist
                failed_lines.append(line)
                continue
            try:
                product, created = Product.objects.get_or_create(
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
                raise

            if(created):
                products_added += 1
            else:
                failed_lines.append(line)
        row_num += 1

    return products_added, failed_lines


def get_random_prod(user):
    curr_person = get_object_or_404(Person, user=user)
    curr_preferences = PersPref.objects.filter(user=curr_person)

    # loads possible bought with products eligible to be bought based on
    # user preferences.
    possible_bought = []
    for pref in curr_preferences:
        tagword_list = pref.tagwords.split(",")
        for tagword in tagword_list:
            possible_bought.extend(Products.objects.filter(
                                   description_contains=tagword
                                   ).filter(category=pref.category))
    from random import choice
    to_be_bought = choice(possible_bought)

    return to_be_bought
