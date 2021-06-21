
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from .models import *

import logging


class ObjectDetailMixin:
    model = None
    template = None

    def get(self, request, slug):
        logging.debug(f"get request of detail {self.model.__name__} {slug}")
        obj = get_object_or_404(self.model, slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj, 'admin_object': obj, 'detail': True})


class ObjectCreateMixin:
    form_model = None
    template = None

    def get(self, request):
        form = self.form_model()
        logging.debug(f"get request of {self.form_model.__name__} creation {request.GET['title']}")
        return render(request, self.template, context={'form': form})

    def post(self, request):
        bound_form = self.form_model(request.POST, request.FILES)
        logging.debug(f"POST request of {self.form_model.__name__} creation {request.POST['title']}")

        if (bound_form.is_valid() and request.FILES.get('input') is not None and request.FILES.get('input').name.endswith('.txt')
         and request.FILES.get('output') is not None and request.FILES.get('output').name.endswith('.txt')):
            new_obj = bound_form.save()
            logging.debug(f"successful POST")
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form})


class ObjectUpdateMixin:
    model = None
    model_form = None
    template = None

    def get(self, request, slug):
        logging.debug(f"get request of {self.model.__name__} update {slug}")
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(instance=obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})

    def post(self, request, slug):
        obj = self.model.objects.get(slug__iexact=slug)
        bound_form = self.model_form(request.POST, instance=obj)
        logging.debug(f"POST request of {self.model.__name__} update {slug}")

        if bound_form.is_valid():
            logging.debug(f"successful POST")
            new_obj = bound_form.save()
            return redirect(new_obj)
        return render(request, self.template, context={'form': bound_form, self.model.__name__.lower(): obj})


class ObjectDeleteMixin:
    model = None
    template = None
    redirect_url = None

    def get(self, request, slug):
        logging.debug(f"get request of {self.model.__name__} delete {slug}")
        obj = self.model.objects.get(slug__iexact=slug)
        return render(request, self.template, context={self.model.__name__.lower(): obj})

    def post(self, request, slug):
        logging.debug(f"POST request of {self.model.__name__} delete {slug}")
        obj = self.model.objects.get(slug__iexact=slug)
        obj.delete()
        return redirect(reverse(self.redirect_url))