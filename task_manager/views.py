from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render


def index(request):
    return render(request, 'base.html')



class IndexView(TemplateView):
    """Home page"""
    template_name = "index.html"
