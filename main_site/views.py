from myrchme.main_site.models import *
from myrchme.main_site.my_forms import *
from django.forms.models import inlineformset_factory

#HTTP rendering tools
from django.shortcuts import render_to_response, get_object_or_404, redirect
#from django.http import HttpResponse, HttpResponseRedirect

#Django Authentication stuff
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
#from django.contrib.auth.forms import SetPasswordForm, UserCreationForm, UserChangeForm

#from myrchme.main_site.forms import *



def index(request):
    """
    index:
    Main page logic.
    """
    curr_user = request.user

    return render_to_response('base/index.html', {'curr_user':curr_user})


def register_person(request):
    """
    registerPerson:
    """
    if request.user.id:
        return redirect('/profile.html')

    #handles registration form, registers user
    if request.method == 'POST':
        #get form
        form = RegisterForm(request.POST)
        #if from is valid, add the user and log them in
        if form.is_valid():
                form.save(request=request)
                user = authenticate(username=form.cleaned_data["username"],
                                    password=form.cleaned_data["password"])
                login(request, user)
                return redirect('/profile.html')
        else:
                form.error = "Form error."

    else:
        #request is a GET (seeing page for 1st time)
        form = RegisterForm()
        
    return render_to_response('base/register.html', {'form':form})


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
        #pers_pref = PersPref(user=curr_person)
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
                {'preferences':preferences, 'pref_form':pref_form, 'errors':pref_form.errors})

        

