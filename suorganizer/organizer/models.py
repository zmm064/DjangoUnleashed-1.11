from datetime import date

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

class Tag(models.Model):
    name = models.CharField(max_length=31, unique=True)
    slug = models.SlugField(max_length=31, unique=True, help_text='A label for URL config')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

    def published_post(self):
        return self.blog_post.filter(pub_date__lt=date.today())

    def get_absolute_url(self):
        return reverse('organizer:tag_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizer:tag_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer:tag_delete', kwargs={'slug': self.slug})


class Startup(models.Model):
    name         = models.CharField(max_length=31, db_index=True)
    slug         = models.SlugField(max_length=31, unique=True, help_text='A label for URL config')
    description  = models.TextField()
    founded_date = models.DateField(verbose_name='date founded')
    contact      = models.EmailField()
    website      = models.URLField(max_length=255)

    tags         = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        get_latest_by = 'founded_date'

    def published_posts(self):
        return self.blog_posts.filter(pub_date__lt=date.today())

    def get_absolute_url(self):
        return reverse('organizer:startup_detail', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('organizer:startup_update', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('organizer:startup_delete', kwargs={'slug': self.slug})


class NewsLink(models.Model):
    title    = models.CharField(max_length=63)
    pub_date = models.DateField(verbose_name='date published')
    link     = models.URLField(max_length=255)

    startup  = models.ForeignKey(Startup)

    def __str__(self):
        return "{}:{}".format(self.startup, self.title)

    class Meta:
        verbose_name  = 'news article'
        ordering      = ['-pub_date']
        get_latest_by = 'pub_date'

    def get_absolute_url(self):
        return self.startup.get_absolute_url()

    def get_update_url(self):
        return reverse('organizer:newslink_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('organizer:newslink_delete', kwargs={'pk': self.pk})