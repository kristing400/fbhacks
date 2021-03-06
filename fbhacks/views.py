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
def event_info(request):
    template = loader.get_template("event_info.html")
    return HttpResponse(template.render())

@csrf_exempt
def event_summary(request):
    template = loader.get_template("event_summary.html")
    return HttpResponse(template.render())
