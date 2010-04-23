from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'myrchme.main_site.views.index'),
    (r'^register$', 'myrchme.main_site.views.register_person'),
    (r'^register-vendor$', 'myrchme.main_site.views.register_vendor'),
    (r'^profile$', 'myrchme.main_site.views.view_person_profile'),
    (r'^store-profile$', 'myrchme.main_site.views.view_store_profile'),
    (r'^preferences$', 'myrchme.main_site.views.set_preferences'),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
