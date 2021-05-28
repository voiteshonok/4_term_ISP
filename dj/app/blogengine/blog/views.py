from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views import View

from .models import Post, Tag
from .utils import ObjectDetailMixin

# Create your views here.
def posts_list(request):
    posts = Post.objects.all()
    return render(request, "blog/index.html", context={'posts': posts})


class PostDeteil(ObjectDetailMixin, View):
    model = Post
    template = 'blog/post_detail.html'


class TagDEtail(ObjectDetailMixin, View):
    dmodel = Post
    template = 'blog/tag_detail.html'


def tags_list(request):
    tags = Tag.objects.all()
    return render(request, 'blog/tags_list.html', context={'tags': tags})

