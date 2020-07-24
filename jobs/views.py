from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from .models import Job


class IndexView(TemplateView):
    template_name = "index.html"


class JobsView(ListView):
    model = Job
    template_name = "jobs.html"
    paginate_by = 50
