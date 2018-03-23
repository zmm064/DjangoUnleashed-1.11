from django.conf.urls import url
from .views import PostList, post_detail, PostCreate, PostUpdate, PostDelete, PostArchiveYear, PostArchiveMonth


urlpatterns = [
    url(r'^$', PostList.as_view(), name='post_list'),
    url(r'^(?P<year>\d{4})/$', PostArchiveYear.as_view(), name='post_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',PostArchiveMonth.as_view(), name='post_archive_month'),

    url(r'^(?P<year>\d{4})/'
        r'(?P<month>\d{1,2})/'
        r'(?P<slug>[\w\-]+)/$', post_detail, name='post_detail'),

    url(r'^create/$', PostCreate.as_view(), name='post_form_create'),
    url(r'^(?P<year>\d{4})/'
        r'(?P<month>\d{1,2})/'
        r'(?P<slug>[\w\-]+)/update/$', PostUpdate.as_view(), name='post_update'),
    url(r'^(?P<year>\d{4})/'
        r'(?P<month>\d{1,2})/'
        r'(?P<slug>[\w\-]+)/delete/$', PostDelete.as_view(), name='post_delete'),
    ]
