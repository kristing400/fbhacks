from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.shortcuts import redirect
from django.template import loader
import os
import json

@csrf_exempt
def index(request):
    template = loader.get_template("index.html")
    return HttpResponse(template.render())

@csrf_exempt
def in_progress(request):
    template = loader.get_template("in_progress.html")
    return HttpResponse(template.render())
