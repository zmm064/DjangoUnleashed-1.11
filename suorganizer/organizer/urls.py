from django.conf.urls import url
from .views import (startup_detail, StartupList, tag_detail, TagList, TagPageList,
                    TagCreate, StartupCreate, NewsLinkCreate,
                    TagUpdate, StartupUpdate, NewsLinkUpdate,
                    TagDelete, StartupDelete, NewsLinkDelete,)


urlpatterns = [
    url(r'^newslink/create/$', NewsLinkCreate.as_view(), name='newslink_create' ),
    url(r'^newslink/update/(?P<pk>\d+)/$', NewsLinkUpdate.as_view(), name='newslink_update'),
    url(r'^newslink/delete/(?P<pk>\d+)/$', NewsLinkDelete.as_view(), name='newslink_delete'),

    url(r'^startup/$', StartupList.as_view(), name='startup_list'),
    url(r'^startup/create/$', StartupCreate.as_view(), name='startup_form_create'),
    url(r'^startup/(?P<slug>[\w\-]+)/$', startup_detail, name='startup_detail'),
    url(r'^startup/(?P<slug>[\w\-]+)/update/$', StartupUpdate.as_view(), name='startup_update'),
    url(r'^startup/(?P<slug>[\w\-]+)/delete/$', StartupDelete.as_view(), name='startup_delete'),

    url(r'^tag/$', TagList.as_view(), name='tag_list'),
    url(r'^tag/(?P<page_number>\d+)/$', TagPageList.as_view(), name='tag_page'),
    url(r'^tag/create/$', TagCreate.as_view(), name='tag_form_create'),
    url(r'^tag/(?P<slug>[\w\-]+)/$', tag_detail, name='tag_detail'),
    url(r'^tag/(?P<slug>[\w\-]+)/update/$', TagUpdate.as_view(), name='tag_update'),
    url(r'^tag/(?P<slug>[\w\-]+)/delete/$', TagDelete.as_view(), name='tag_delete'),
]
