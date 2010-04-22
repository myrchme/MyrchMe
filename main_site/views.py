from myrchme.main_site.models import *

#HTTP rendering tools
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect

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
    return render_to_response('base/index.html')


def register(request):
    """
    register:
    """
    if request.user.id:
        return redirect('/profile.html')

    #handles registration form, registers user
    if request.method == 'POST':
        #get form
        form = RegisterForm(request.POST)
        #if from is valid, add the user and log them in
        if form.is_valid():
                new_user = form.save(request=request)
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