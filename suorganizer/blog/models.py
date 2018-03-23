from django.db import models
from django.core.urlresolvers import reverse

from organizer.models import Startup, Tag


class Post(models.Model):
    title    = models.CharField(max_length=63)
    slug     = models.SlugField(max_length=63, help_text='A label for URL config', unique_for_month='pub_date')
    text     = models.TextField()
    pub_date = models.DateField(verbose_name='date published', auto_now_add=True)
    
    tags     = models.ManyToManyField(Tag, related_name='blog_posts')
    startups = models.ManyToManyField(Startup, related_name='blog_posts')

    def __str__(self):
        return "{} on {}".format(self.title, self.pub_date.strftime('%Y-%m-%d'))

    class Meta:
        verbose_name  = 'blog post'
        ordering      = ['-pub_date', 'title']
        get_latest_by = 'pub_date'

    def get_absolute_url(self):
        return reverse('blog:post_detail', 
                       kwargs={'year' : self.pub_date.year, 
                               'month': self.pub_date.month,
                               'slug' : self.slug})

    def get_update_url(self):
        return reverse('blog:post_update',
                       kwargs={'year' : self.pub_date.year, 
                               'month': self.pub_date.month,
                               'slug' : self.slug})

    def get_delete_url(self):
        return reverse('blog:post_delete',
                       kwargs={'year' : self.pub_date.year, 
                               'month': self.pub_date.month,
                               'slug' : self.slug})

    def get_archive_year_url(self):
        return reverse('blog_post_archive_year', kwargs={'year': self.pub_date.year})

    def get_archive_month_url(self):
        return reverse('blog_post_archive_month', kwargs={
            'year': self.pub_date.year, 
            'month': self.pub_date.month
            })