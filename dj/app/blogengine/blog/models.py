from django.db import models
from django.db.models.fields import CharField
from django.shortcuts import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.conf import settings

from time import time

def gen_slug(s):
    new_slug = slugify(s, allow_unicode=True)
    return f"{new_slug}-{str(int(time()))}"


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    body = models.TextField(null=False, blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='posts')
    input = models.FileField(null=False, blank=True)
    output = models.FileField(null=False, blank=True)
    time_limit = models.FloatField(null=False, default=1)
    memory_limit = models.IntegerField(null=False, default=256 * 1024 * 1024)


    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):

        if not self.id:
            self.slug = gen_slug(self.title)
        super().save(*args, **kwargs)

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['-date_pub']


class Tag(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def get_absolute_url(self):
        return reverse('tag_detail_url', kwargs={"slug": self.slug})

    def __str__(self):
        return f'{self.title}'

    def get_delete_url(self):
        return reverse('tag_delete_url', kwargs={"slug": self.slug})

    def get_update_url(self):
        return reverse('tag_update_url', kwargs={'slug': self.slug})

    class Meta:
        ordering = ['title']


class Submit(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_pub = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Post, on_delete=models.CASCADE)
    code = models.TextField(null=False, blank=True)
    verdict = models.TextField(null=False, blank=True)

    def __str__(self):
        return f'{self.author} {self.task} {self.date_pub}'