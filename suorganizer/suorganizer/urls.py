"""
Definition of urls for suorganizer.
"""

from django.conf.urls import include, url
from django.views.generic import RedirectView
from django.contrib import admin
from django.contrib.flatpages import urls as flatpages_urls
from .views import redirect_root
# admin.autodiscover()


urlpatterns = [
    # Examples:
    # url(r'^$', suorganizer.views.home, name='home'),
    # url(r'^suorganizer/', include('suorganizer.suorganizer.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(pattern_name='blog:post_list',permanent=False)),
    url(r'^blog/', include('blog.urls', namespace='blog', app_name='blog')),
    url(r'^contact/', include('contact.urls')),
    #url(r'^page/', include(flatpages_urls)),
    url(r'^', include('organizer.urls', namespace='organizer', app_name='organizer')),
    url(r'^', include(flatpages_urls)),
]
