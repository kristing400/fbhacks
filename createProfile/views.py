from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from . import speechToText
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def index(request):
    if request.method == 'POST':
        if len(request.FILES):
            fileObj = request.FILES['filee']
            text = speechToText.main(fileObj)
        else:
            print("no file")
        return HttpResponse(text)
    template = loader.get_template("createProfile/index.html")
    return HttpResponse(template.render())