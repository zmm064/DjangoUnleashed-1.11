from django.conf.urls import url
from .views import startup_detail, startup_list, tag_detail, tag_list


urlpatterns = [
    url(r'^startup/$', startup_list, name='startup_list'),
    url(r'^startup/(?P<slug>[\w\-]+)/$', startup_detail, name='startup_list'),
    url(r'^tag/$', tag_list, name='tag_list'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', tag_detail, name='tag_detail')
]
