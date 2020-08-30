from django.shortcuts import render
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):
    template_name = 'core/home.html'

    def get(self, request, *args, **kwargs):  # para anadir datos al diccionario de contexto
        return render(request, self.template_name, {'title': 'Mi super Web Playground'})

class SamplePageView(TemplateView):
    template_name = 'core/sample.html'