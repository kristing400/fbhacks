from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from . import speechToText
from . import parser
from django.views.decorators.csrf import csrf_exempt
import json
import os
# Create your views here.
convoCounter = 0
@csrf_exempt
def index(request):
    template = loader.get_template("createProfile/index.html")
    return HttpResponse(template.render())
@csrf_exempt
def getKeywords(request):
    global convoCounter
    maxCounter = 4
    dirpath = os.path.dirname(os.path.realpath(__file__))
    with open(dirpath + '/db.json') as src:
        db = json.load(src)
        print(db)
    if request.method == 'POST':
        if len(request.FILES):
            fileObj = request.FILES['filee']
            text = speechToText.main(fileObj)
            if 'convo' not in db:
                db['convo'] = ""
            if text:
                db['convo'] = db['convo'] + " " + text
                if convoCounter == maxCounter:
                    keywords = parser.main(db['convo'])
                    if 'text' not in db:
                        db['text'] = []
                    print(keywords)
                    db['text'] = db['text'] + keywords
                    convoCounter = 0
                    db['convo'] = ""
                else:
                    convoCounter += 1
        else:
            print("no file")
        with open(dirpath + '/db.json', 'w+') as outfile:
            json.dump(db, outfile)
    return HttpResponse(db)
