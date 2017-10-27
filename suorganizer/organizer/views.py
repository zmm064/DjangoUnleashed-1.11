from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View

from .models import Startup, Tag, NewsLink
from .forms import TagForm, StartupForm, NewsLinkForm
from .utils import ObjectCreateMixin, ObjectUpdateMixin, ObjectDeleteMixin
# Create your views here.

def startup_detail(request, slug):
    startup = get_object_or_404(Startup, slug__iexact=slug)
    return render(request, 
                  'organizer/startup_detail.html',
                  {'startup': startup})

def startup_list(request):
    return render(request,
                  'organizer/startup_list.html',
                  {'startup_list': Startup.objects.all()})

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug__iexact=slug)
    return render(request,
                  'organizer/tag_detail.html',
                  {'tag': tag})

def tag_list(request):
    return render(request,
                  'organizer/tag_list.html',
                  {'tag_list': Tag.objects.all()})


class TagCreate(View, ObjectCreateMixin):
    form_class = TagForm
    template_name = 'organizer/tag_form_create.html'


class StartupCreate(View, ObjectCreateMixin):
    form_class = StartupForm
    template_name = 'organizer/startup_form_create.html'


class NewsLinkCreate(View, ObjectCreateMixin):
    form_class = NewsLinkForm
    template_name = 'organizer/startup_form_create.html'


class NewsLinkUpdate(View, ObjectUpdateMixin):
    form_class = NewsLinkForm
    template_name = 'organizer/newslink_form_update.html'

    def get(self, request, pk):
        newslink = get_object_or_404(NewsLink, pk=pk)
        return render(request, 
                      self.template_name,
                      {'form': self.form_class(instance=newslink), 'newslink': newslink})

    def post(self, request, pk):
        newslink = get_object_or_404(NewsLink, pk=pk)
        bound_form = self.form_class(request.POST, instance=newslink)
        if bound_form.is_valid():
            new_newslink = bound_form.save()
            return redirect(new_newslink)
        else:
            return render(request, 
                          self.template_name,
                          {'form': bound_form, 'newslink': newslink})


class TagUpdate(View, ObjectUpdateMixin):
    form_class    = TagForm
    model         = Tag
    template_name = 'organizer/tag_form_update.html'


class StartupUpdate(View, ObjectUpdateMixin):
    form_class    = StartupForm
    model         = Startup
    template_name = 'organizer/startup_form_update.html'


class NewsLinkDelete(View):
    def get(self, request, pk):
        newslink = get_object_or_404(NewsLink, pk=pk)
        return render(request, 'organizer/newslink_form_delete.html', {'newslink': newslink})

    def post(self, request, pk):
        newslink = get_object_or_404(NewsLink, pk=pk)
        startup = newslink.startup
        newslink.delete()
        return redirect(startup)


class TagDelete(View, ObjectDeleteMixin):
    model         = Tag
    success_url   = reverse_lazy('organizer:tag_list')
    template_name = 'organizer/tag_form_delete.html'


class StartupDelete(View, ObjectDeleteMixin):
    model         = Startup
    success_url   = reverse_lazy('organizer:startup_list')
    template_name = 'organizer/startup_form_delete.html'