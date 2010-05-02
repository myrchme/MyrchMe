from django.conf.urls.defaults import *

urlpatterns = patterns('myrchme.main_site.views', #views prefix shortcut
    (r'^$', 'index'),
    (r'^logout$', 'logout_view'),
    (r'^register$', 'register_person'),
    (r'^register-vendor$', 'register_vendor'),

    #Public URLs
    (r'^store/(?P<username>.*)$', 'view_store'),
    (r'^user/(?P<username>.*)$', 'view_person_profile'),
    (r'^product/(?P<id>.*)$*)$', 'view_product'),
    
    #Person URLs
    (r'^buy/(?P<id>.*)$', 'buy_view'), #TODO: make this SEO-friendly, use slugs
    (r'^account$', 'change_person_account'),
    (r'^preferences$', 'set_preferences'),

    #Vendor URLs
    (r'^store-profile$', 'view_my_store_profile'),
    (r'^inventory$', 'view_inventory'),
    (r'^upload$', 'upload_products_view')

)