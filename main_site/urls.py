from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'myrchme.main_site.views.index'),
    (r'^register$', 'myrchme.main_site.views.register_person'),
    (r'^register-vendor$', 'myrchme.main_site.views.register_vendor'),
    (r'^profile$', 'myrchme.main_site.views.view_person_profile'),
    (r'^store-profile$', 'myrchme.main_site.views.view_my_store_profile'),
    (r'^preferences$', 'myrchme.main_site.views.set_preferences'),
    (r'^logout$', 'myrchme.main_site.views.logout_view'),
    (r'^account$', 'myrchme.main_site.views.change_person_account')

)