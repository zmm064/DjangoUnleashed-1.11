from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy


password_urls = [
    url(r'^change/$',
        auth_views.password_change,
        {'template_name': 'user/password_change_form.html',
         'post_change_redirect': reverse_lazy('dj-auth:pw_change_done')},
        name='pw_change'),
    url(r'^change/done/$',
        auth_views.password_change_done,
        {'template_name': 'user/password_change_done.html'},
        name='pw_change_done'),
]

urlpatterns = [
    url(r'^login/$', auth_views.login, {
            'template_name': 'user/login.html'
            }, name='login'),
    # Add AuthenticationForm to the context 
    # of the logged_out.html template
    url(r'^logout/$', auth_views.logout, {
            'template_name': 'user/logged_out.html', 
            'extra_context': {'form': AuthenticationForm}
            }, name='logout'),
    url(r'^$', RedirectView.as_view(pattern_name='dj-auth:login', permanent=False)),
    url(r'^password/', include(password_urls)),
]
