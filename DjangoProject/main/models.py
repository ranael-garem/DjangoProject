from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template.defaultfilters import slugify


class Library(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    owner = models.ForeignKey(User)


class Book(models.Model):
    """
    A single Book entry

    """
    name = models.CharField(max_length=128)
    author = models.CharField(max_length=100)
    slug = models.SlugField(unique=False, default='slug')
    library = models.ForeignKey(Library, null=True)

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
            self.slug = slugify(self.name)
            super(Book, self).save(*args, **kwargs)


class Notification(models.Model):
    message = models.CharField(max_length=300)
    library = models.ForeignKey(Library, null=True)
    book = models.ForeignKey(Book, null=True)
    read = models.BooleanField(default=False)
    owner = models.ForeignKey(User, null=True, related_name='owner')
    slug = models.CharField(max_length=100, default='default')
    user = models.ForeignKey(User, null=True, related_name='user')
