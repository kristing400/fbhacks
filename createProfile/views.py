from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from . import speechToText
from django.views.decorators.csrf import csrf_exempt
import json
import os
# Create your views here.
@csrf_exempt
def index(request):
    template = loader.get_template("createProfile/index.html")
    return HttpResponse(template.render())
@csrf_exempt
def getKeywords(request):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    with open(dirpath + '/db.json') as src:
        db = json.load(src)
        print(db)
    if request.method == 'POST':
        if len(request.FILES):
            fileObj = request.FILES['filee']
            text = speechToText.main(fileObj)
            if 'text' not in db:
                db['text'] = []
            db['text'].append(text)
        else:
            print("no file")
        with open(dirpath + '/db.json', 'w+') as outfile:
            json.dump(db, outfile)
    return HttpResponse(db)
