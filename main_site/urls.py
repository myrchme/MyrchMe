from django.conf.urls.defaults import *

urlpatterns = patterns('myrchme.main_site.views', #views prefix shortcut
    (r'^$', 'index'),
    (r'^logout$', 'logout_view'),
    (r'^register$', 'register_person'),
    (r'^register-vendor$', 'register_vendor'),

    #Public URLs
    (r'^store/(?P<username>.*)$', 'view_store'),
    (r'^user/(?P<username>.*)$', 'view_person_profile'),
    (r'^product/(?P<id>.*)$', 'view_product'),
    
    #Person-only URLs
    (r'^buy/(?P<id>.*)$', 'buy_view'), #TODO: make this SEO-friendly, use slugs
    (r'^account$', 'update_person_account'),
    (r'^credit-card$', 'update_credit_card'),
    (r'^preferences$', 'update_preferences'),
    (r'^delete-all-prefs$', 'delete_all_prefs'),

    #Vendor-only URLs
    (r'^store-profile$', 'view_my_store_profile'),
    (r'^inventory$', 'view_inventory'),
    (r'^delete-all-prods$', 'delete_all_prods'),

    (r'^upload$', 'upload_products_view'),
)