from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from django.http import Http404, JsonResponse
from .models import Thread, Message
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.urls import reverse_lazy


@method_decorator(login_required, name="dispatch")
class ThreadList(TemplateView):
    template_name = "messenger/thread_list.html"


@method_decorator(login_required, name="dispatch")
class ThreadDetail(DetailView):
    model = Thread
    
    def get_object(self):  # se sobreescribe el metodo para poder manipular el queryset
        obj = super(ThreadDetail, self).get_object()  # obteniendo la instancia
        if self.request.user not in obj.users.all():  # filtrando
            raise Http404()
        return obj
