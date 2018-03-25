from django.views.generic import UpdateView as BaseUpdateView


class UpdateView(BaseUpdateView):
    # 继承自定义的UpdateView方法
    template_name_suffix = '_form_update'
