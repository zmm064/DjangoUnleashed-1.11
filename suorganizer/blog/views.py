from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from django.views.generic import View

# Create your views here.
from .models import Post
from .forms import PostForm

@require_http_methods(['HEAD', 'GET'])
def post_detail(request, year, month, slug):
    post = get_object_or_404(Post, 
                             pub_date__year=year, pub_date__month=month, slug=slug)
    return render(request, 
                  'blog/post_detail.html',
                  {'post': post})


class PostList(View):
    def get(self, request):
        return render(request, 
                      'blog/post_list.html',
                      {'post_list': Post.objects.all()})


class PostCreate(View):
    form_class = PostForm
    template_name = 'blog/post_form_create.html'

    def get(self, request):
        return render(request, 
                      self.template_name, 
                      {'form': self.form_class()})

    def post(self, request):
        bound_form = self.form_class(request.POST)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        else:
            return render(request,
                          self.template_name,
                          {'form': bound_form})


class PostUpdate(View):
    # why:为什么这样能实现博客的修改而非新增?
    form_class = PostForm
    model = Post
    template_name = 'blog/post_form_update.html'

    def get(self, request, year, month, slug):
        post = get_object_or_404(self.model, 
                                 pub_date__year=year, pub_date__month=month, slug=slug)
        return render(request,
                      self.template_name,
                      {'form': self.form_class(instance=post), 'post': post})

    def post(self, request, year, month, slug):
        post = get_object_or_404(self.model, 
                                 pub_date__year=year, pub_date__month=month, slug=slug)
        bound_form = self.form_class(request.POST, instance=post)
        if bound_form.is_valid():
            new_post = bound_form.save()
            return redirect(new_post)
        else:
            return render(request,
                          self.template_name,
                          {'form': bound_form, 'post': post})


class PostDelete(View):
    model = Post
    template_name = 'blog/post_form_delete.html'

    def get(self, request, year, month, slug):
        post = get_object_or_404(self.model, 
                                 pub_date__year=year, pub_date__month=month, slug=slug)
        return render(request, self.template_name, {'post': post})

    def post(self, request, year, month, slug):
        post = get_object_or_404(self.model, 
                                 pub_date__year=year, pub_date__month=month, slug=slug)
        post.delete()
        return redirect('blog:post_list')

