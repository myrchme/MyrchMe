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
    index
    Main page logic.
    """
    return render_to_response('base/index.html')