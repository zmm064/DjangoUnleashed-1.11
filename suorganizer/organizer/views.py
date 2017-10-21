from django.shortcuts import render, get_object_or_404
from .models import Startup, Tag
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
