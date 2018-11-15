from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from . import speechToText
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
i = 0
@csrf_exempt
def index(request):
    global i
    i += 1
    if request.method == 'POST':
        if len(request.FILES):
            fileObj = request.FILES['filee']
            text = speechToText.main(fileObj)
        else:
            print("no file")
    template = loader.get_template("createProfile/index.html")
    return HttpResponse(template.render({"text": i}))
