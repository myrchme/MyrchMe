# Create your views here.
#HTTP rendering tools
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from myrchme.main_site.models import *

#Django Authentication stuff
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import SetPasswordForm, UserCreationForm, UserChangeForm

from django.forms.models import modelformset_factory

from django.template import RequestContext


from myrchme.main_site.forms import *


from django.utils.encoding import *



def index(request):

    """
    index

    Main page logic. Displays top 5 rants.

    """