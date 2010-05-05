from django.contrib.auth import logout
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.core import serializers
from myrchme.main_site.models import *
from myrchme.main_site.my_forms import *
from myrchme.main_site.helpers import *
from myrchme import settings
from cgi import escape


def index(request):
    """
    index: Main page logic.
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
def update_person_account(request):
    """
    update_person_account:
    Displays and processes form for editing basic person info.
    """
    curr_person = get_object_or_404(Person, user=request.user)

    if request.method == 'POST':
        accountform = AccountForm(request.POST)
        addressform = AddressForm(request.POST)
        if accountform.is_valid():
            accountform.save(request.user)
        if addressform.is_valid():
            addressform.update_acc_address(request.user)
    else:
        #initialize form fields with curr_person data
        accountform = AccountForm(instance=curr_person)
        addressform = AddressForm(instance=curr_person.shipping_address)

    account_dict = {'accountform':accountform,
                    'addressform':addressform,
                    'user':request.user
    }
    return render_to_response('base/user/account.html', account_dict)


@user_login_required(user_type='Person')
def update_credit_card(request):
    """
    update_credit_card:
    Displays and processes form for editing credit card info.
    """
    curr_person = get_object_or_404(Person, user=request.user)

    if request.method == 'POST':
        cc_form = CreditCardForm(request.POST)
        cc_add_form = AddressForm(request.POST)
        if cc_form.is_valid():
            cc_form.save(request.user)
        if cc_add_form.is_valid():
            cc_add_form.update_cc_address(request.user)
    else:
        cc_form = CreditCardForm(instance=curr_person.credit_card)
        try:
            cc_add_form = AddressForm(
                            instance=curr_person.credit_card.billing_address)
        except AttributeError:  #catches the case when the user has no CC yet
            cc_add_form = AddressForm()

    cc_dict = {'cc_form':cc_form,
               'cc_add_form':cc_add_form,
               'user':request.user
    }
    return render_to_response('base/user/credit_card.html', cc_dict)


def view_person_profile(request, username): #request MUST be an arg here or
                                            #function fails
    """
    view_person_profile: Displays a Person's public profile
    """
    #escape() used to sanitize user input
    curr_person = get_object_or_404(Person, username=escape(username))
    preferences = PersPref.objects.filter(user=curr_person)
    #only display gifts that have been delivered so we don't ruin the surprise
    transactions = Transaction.objects.filter(buyer=curr_person).filter(
                                                             status='DELIVERED')
    profile_dict= { 'person':curr_person,
                    'preferences':preferences,
                    'transactions':transactions,
                    'user':request.user
    }
    return render_to_response('base/user/profile.html', profile_dict)


@user_login_required(user_type='Vendor')
def view_my_store_profile(request):
    """
    view_my_store_profile: Displays Vendor's internal (non-public) profiles.
    """
    curr_vendor = get_object_or_404(Vendor, user=request.user)
    transactions = Transaction.objects.filter(vendor=curr_vendor
                                            ).exclude(status='FAILED')
    profile_dict = {'vendor':curr_vendor,
                    'transactions':transactions,
                    'user': request.user
    }
    
    return render_to_response('base/store/store_profile.html', profile_dict)


def view_store(request, username):
    """
    view_store: Displays public storefront, with store's products.
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
def update_preferences(request):
    """
    update_preferences: Displays a form for adding and deleting PersPrefs.
    """
    curr_person = get_object_or_404(Person, user=request.user)
    preferences = PersPref.objects.filter(user=curr_person)
    pref_form = PreferenceForm()
    
    if request.method == 'POST':
        pref_form = PreferenceForm(request.POST)
        if pref_form.is_valid():
            pref_form.save(request.user)
            message = "Preferences successfully saved."
            return render_to_response('base/user/preferences.html',
                {'preferences':preferences, 'form':pref_form,
                 'message':message, 'user':request.user})

    pref_dict = {'preferences':preferences,
                 'form':pref_form,
                 'errors':pref_form.errors,
                 'user':request.user
    }        
    return render_to_response('base/user/preferences.html', pref_dict)


@user_login_required(user_type='Person')
def delete_all_prefs(request):
    """
    delete_all_prefs: Delete all of a Person's preferences.
    """
    curr_person = get_object_or_404(Person, user=request.user)
    PersPref.objects.filter(user=curr_person).delete()
    return redirect ('/preferences')


def logout_view(request):
    logout(request)
    return redirect('/')


@user_login_required(user_type='Person')
def buy_view(request, id):
    """
    buy_view:
    Creates a transaction object, serializes it to a JSON object, and sends
    to vendor's remote server for completion.
    """
    product = get_object_or_404(Product, id=int(escape(id)))
    person = get_object_or_404(Person, user=request.user)
    message = buy(person, product)
    results_dict = {'message': message, 'user':request.user}

    return render_to_response('base/user/buy_results.html', results_dict)


def api_receive_transaction(request):
    """
    api_receive_transaction:
    This function allows vendors to update their transactions
    """
    if request.method == 'POST':
        data = request.POST["JSON"]
        json = serializers.deserialize("json", data)
        #this part is yet to be developed
        #vendor = get_object_or_404(Vendor, api_key = json.["api_key"])
        #transaction = get_object_or_404(Transaction, id = json.["transaction_id"])
        #update transaction status here
        return redirect ('/404')
    else:
        return redirect ('/404')


@user_login_required(user_type='Vendor')
def view_inventory(request):
    """
    view_inventory: Displays a Vendor's inventory.
    """
    curr_vendor = get_object_or_404(Vendor, user=request.user)
    products = Product.objects.filter(vendor=curr_vendor)
    invt_dict = {'products':products, 'user':request.user}

    return render_to_response('base/store/inventory.html', invt_dict)


@user_login_required(user_type='Vendor')
def delete_all_prods(request):
    """
    delete_all_prods: Delets all products in a vendor's inventory.
    """
    curr_vendor = get_object_or_404(Vendor, user=request.user)
    Product.objects.filter(vendor=curr_vendor).delete()
    return redirect('/inventory')


def view_product(request, id):
    """
    view_product: Displays product details page.
    """
    product = get_object_or_404(Product, id=id)
    prod_dict = {'product':product, 'user':request.user}
    
    return render_to_response('base/product_details.html', prod_dict)


@user_login_required(user_type='Vendor')
def upload_products_view(request):
    """
    Displays and processes form for uploading tab-delimited txt files that
    contain a Vendor's products.
    """
    curr_vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
           folderpath = settings.UPLOAD_DIR + "vendor/"
           filepath = save_file(request.FILES['file'], folderpath,
                                request.user.username)
           #this line is where products are added to the db
           num_added, failed_lines = upload_products(filepath, curr_vendor)
           results_dict = {'num_added':num_added,
                           'failed_lines':failed_lines,
                           'user':request.user}
           return render_to_response('base/store/upload_results.html',
                                     results_dict)
    else:
        form = UploadFileForm()
        form_dict = {'form': form,'user':request.user}
        return render_to_response('base/store/upload.html', form_dict)