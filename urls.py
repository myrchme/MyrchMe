from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Urls to serve static media: JS,CSS,images,etc
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': '/Users/Ahmed/myrchme/media/'}),

    # Main site urls
    (r'', include('myrchme.main_site.urls')),

    # Django's auto-generated documentation
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    
    # Django's admin backend
    (r'^admin/', include(admin.site.urls))
)
