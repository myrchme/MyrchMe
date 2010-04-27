from django.conf.urls.defaults import *

urlpatterns = patterns('myrchme.main_site.views', #views prefix shortcut
    (r'^$', 'index'),
    (r'^register$', 'register_person'),
    (r'^register-vendor$', 'register_vendor'),

    (r'^user/(?P<username>.*)$', 'view_person_profile'),
    (r'^store/(?P<username>.*)$', 'view_store'),

    (r'^store-profile$', 'view_my_store_profile'),
    (r'^buy/(?P<id>.*)$', 'buy_view'),
    (r'^preferences$', 'set_preferences'),
    (r'^logout$', 'logout_view'),
    (r'^account$', 'change_person_account')

)