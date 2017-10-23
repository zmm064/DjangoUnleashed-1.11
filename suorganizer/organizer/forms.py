from django import forms
from django.core.exceptions import ValidationError

from .models import NewsLink, Startup, Tag


class SlugCleanMixin:
    '''混入类用于添加clean_slug方法'''
    def clean_slug(self):
        new_slug = self.cleaned_data['slug'].lower()
        if new_slug == 'create':
            raise ValidationError('Slug may not be "create".')
        return new_slug


class NewsLinkForm(forms.ModelForm):
    class Meta:
        model = NewsLink
        fields = '__all__'


class StartupForm(forms.ModelForm, SlugCleanMixin):
    class Meta:
        model = Startup
        fields = '__all__'


class TagForm(forms.ModelForm, SlugCleanMixin):
    class Meta:
        model = Tag
        fields = '__all__'

    def clean_name(self):
        return self.cleaned_data['name'].lower()