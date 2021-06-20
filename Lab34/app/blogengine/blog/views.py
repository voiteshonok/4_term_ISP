from django.core import paginator
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.views import View
from django.urls import reverse

from .models import Post, Tag, Submit
from .utils import *
from .forms import TagForm, PostForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse

from django.db.models import Q

from .doc.checker import *

import concurrent.futures


def posts_list(request):
    posts = Post.objects.all()

    paginator = Paginator(posts, 2)

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    is_paginated = page.has_other_pages()

    if page.has_previous():
        prev_url = f"?page={page.previous_page_number()}"
    else:
        prev_url = ""

    if page.has_next():
        next_url = f"?page={page.next_page_number()}"
    else:
        next_url = ""

    context = {
        'page_object': page,
        'is_paginated': is_paginated,
        'next_url': next_url,
        'prev_url': prev_url
    }

    return render(request, "blog/index.html", context=context)


class PostDeteil(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'

    def post(self, request, slug):

        task = self.model.objects.get(slug__iexact=slug)

        ch = Checker(task, request.POST.get('code'))
        
        with concurrent.futures.ThreadPoolExecutor() as executor: 
            verdict = executor.submit(ch.run_submission).result()
        # verdict = ch.run_submission()


        if verdict == verdict.OK:
            messages.success(request, verdict.name)
        else:
            messages.info(request, verdict.name)         

        submit = Submit.objects.create(author=request.user, task=task, code=request.POST.get('code'), verdict=verdict.name)

        return render(request, self.template, context={self.model.__name__.lower(): task, 'admin_object': task, 'detail': True})

class TagDetail(ObjectDetailMixin, View):
    model = Tag
    template = 'blog/tag_detail.html'


class TagCreate(LoginRequiredMixin, View):
    form_model = TagForm
    template = 'blog/tag_create.html'
    raise_exception = True

    def get(self, request):
        form = self.form_model()
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST)

        if bound_form.is_valid():
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


def tags_list(request):
    tags = Tag.objects.all()

    for tag in tags:
        related_posts = Post.objects.filter(tags=tag)
        s = 0
        for post in related_posts:
                s += Submit.objects.filter(task=post, verdict=Verdict.OK.name).count()
        tag.submits = s

    return render(request, 'blog/tags_list.html', context={'tags': tags})


class PostCreate(LoginRequiredMixin, ObjectCreateMixin, View):
    form_model = PostForm
    template = 'blog/post_create_form.html'
    raise_exception = True


class TagUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Tag
    model_form = TagForm
    template = 'blog/tag_update_form.html'
    raise_exception = True
    

class PostUpdate(LoginRequiredMixin, ObjectUpdateMixin, View):
    model = Post
    model_form = PostForm
    template = 'blog/post_update_form.html'
    raise_exception = True


class TagDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Tag
    template = 'blog/tag_delete_form.html'
    redirect_url = 'tags_list_url'
    raise_exception = True


class PostDelete(LoginRequiredMixin, ObjectDeleteMixin, View):
    model = Post
    template = 'blog/post_delete_form.html'
    redirect_url = 'posts_list_url'
    raise_exception = True

