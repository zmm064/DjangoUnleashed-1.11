from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View, CreateView, DetailView, DeleteView, UpdateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from user.decorators import class_login_required, require_authenticated_permission

from .models import Startup, Tag, NewsLink
from .forms import TagForm, StartupForm, NewsLinkForm
from .utils import ObjectUpdateMixin, ObjectDeleteMixin
# Create your views here.


class StartupDetail(DetailView):
    context_object_name = 'startup'
    model               = Startup
    template_name       = 'organizer/startup_detail.html'

    #def get(self, request, slug):
    #    startup = get_object_or_404(Startup, slug__iexact=slug)
    #    return render(request, 
    #                  'organizer/startup_detail.html',
    #                  {'startup': startup})


class TagDetail(DetailView):
    context_object_name = 'tag'
    model               = Tag
    template_name       = 'organizer/tag_detail.html'

    #def get(self, request, slug):
    #    tag = get_object_or_404(Tag, slug__iexact=slug)
    #    return render(request,
    #                  'organizer/tag_detail.html',
    #                  {'tag': tag})





class TagList(View):
    template_name = 'organizer/tag_list.html'

    def get(self, request):
        return render(request,
                      'organizer/tag_list.html',
                      {'tag_list': Tag.objects.all()})


class TagPageList(View):
    template_name = 'organizer/tag_list.html'
    paginate_by = 5

    def get(self, request, page_number): # 就获取page_number的方式有点小变化
        tags = Tag.objects.all()
        paginator = Paginator(tags, self.paginate_by)
        try:
            page = paginator.page(page_number)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
        
        prev_url = reverse('organizer:tag_page', args=[page.previous_page_number()]) if page.has_previous() else None
        next_url = reverse('organizer:tag_page', args=[page.next_page_number()]) if page.has_next() else None

        return render(request,
                      self.template_name,
                      {'tag_list': page, 'paginator': paginator, 
                       'next_page_url': next_url, 'previous_page_url': prev_url})


class StartupList(View):
    page_kwarg    = 'page'
    template_name = 'organizer/startup_list.html'
    paginate_by   = 3

    def get(self, request):
        startups    = Startup.objects.all()
        paginator   = Paginator(startups, self.paginate_by)
        page_number = request.GET.get(self.page_kwarg)
        try:
            page = paginator.page(page_number) 
        except PageNotAnInteger: # 这个page_number可能获取不到
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages) # 请求页数过大返回最后一页的结果

        # DRY:生成当前请求页前后页的相关链接，并用到template中
        prev_url = '?{}={}'.format(self.page_kwarg, page.previous_page_number()) if page.has_previous() else None
        next_url = '?{}={}'.format(self.page_kwarg, page.next_page_number()) if page.has_next() else None
        
        return render(request,
                      self.template_name,
                      {'startup_list': page, 'paginator': paginator, 
                       'next_page_url': next_url, 'previous_page_url': prev_url})


@require_authenticated_permission('organizer.add_tag')
class TagCreate(CreateView):
    form_class    = TagForm
    template_name = 'organizer/tag_form_create.html'


class StartupCreate(CreateView):
    form_class    = StartupForm
    template_name = 'organizer/startup_form_create.html'


class NewsLinkCreate(CreateView):
    form_class    = NewsLinkForm
    template_name = 'organizer/startup_form_create.html'


class NewsLinkUpdate(View):
    form_class    = NewsLinkForm
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

@require_authenticated_permission('organizer.change_tag')
class TagUpdate(UpdateView):
    form_class    = TagForm
    model         = Tag
    template_name = 'organizer/tag_form_update.html'


@require_authenticated_permission('organizer.change_startup')
class StartupUpdate(UpdateView):
    form_class    = StartupForm
    model         = Startup
    template_name = 'organizer/startup_form_update.html'


class NewsLinkDelete(DeleteView):
    model = NewsLink

    def get_success_url(self):
        return self.object.startup.get_absolute_url()
    #def get(self, request, pk):
    #    newslink = get_object_or_404(NewsLink, pk=pk)
    #    return render(request, 'organizer/newslink_form_delete.html', {'newslink': newslink})

    #def post(self, request, pk):
    #    newslink = get_object_or_404(NewsLink, pk=pk)
    #    startup = newslink.startup
    #    newslink.delete()
    #    return redirect(startup)


class TagDelete(DeleteView):
    model         = Tag
    success_url   = reverse_lazy('organizer:tag_list')
    template_name = 'organizer/tag_form_delete.html'


class StartupDelete(DeleteView):
    model         = Startup
    success_url   = reverse_lazy('organizer:startup_list')
    template_name = 'organizer/startup_form_delete.html'