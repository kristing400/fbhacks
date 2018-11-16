from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from . import speechToText
from . import parser
from django.views.decorators.csrf import csrf_exempt
import json
import datetime
import time
import os
# Create your views here.
inConvo = False
yourName = "tiffany"
yourOccupation = "engineer"
yourHome = "fremont"
yourCompany = "facebook"

occupation_types = [
    "engineer", "artist", "designer", "actor", "architecture", "sales", "baker","musician",
    "lawyer", "doctor", "dancer", "manager", "recruiter", "banker", "accountant", "consultant", "teacher",
    "reporter", "professor", "student"]
company_names = [
    "facebook", "airbnb", "google", "microsoft", "amazon", "apple", "salesforce"
]

start_trigger_phrases = [
    "nice to mee you", "my name is", "hi", "hello"
]

end_trigger_phrases = [
    "bye", "see you", "nice meeting you", "goodbye"
]
def isOccupation(s):
    for word in s.split(" "):
        if word in occupation_types:
            return True
    return False
@csrf_exempt
def index(request):
    template = loader.get_template("createProfile/index.html")
    return HttpResponse(template.render())
def editProfiles(request):
    dirpath = os.path.dirname(os.path.realpath(__file__))
    with open(dirpath + '/db.json') as src:
        db = json.load(src)
    for convo in db['convos']:

        keywords = parser.main(convo['text'])
        name = ""
        occupation = ""
        company = ""
        home = ""

        keyPoints = []
        for word in keywords:
            if occupation == "" and word['name'].lower() != yourOccupation and isOccupation(word['name'].lower()):
                print("set occupation", word['name'])
                occupation = word['name']
            elif company == "" and word['name'].lower() != yourCompany and word['name'].lower() in company_names:
                company = word['name']
            elif name == "" and word['type'] == 'PERSON' and word['name'].lower() != yourName and not isOccupation(word['name']):
                name = word['name']
            elif home == "" and word['type'] == 'LOCATION' and word['name'].lower() != yourHome:
                home = word['name']
            else:
                keyPoints.append(word['name'])

        newContact = {
            'name': name,
            'occupation': occupation,
            'home': home,
            'company': company,
            'keywords': keyPoints,
            'startTime': convo['startTime'],
            'endTime': convo['endTime']
        }

        db['contacts'].append(newContact)
    db['convos'] = []
    with open(dirpath + '/db.json', 'w+') as outfile:
        json.dump(db, outfile)

    template = loader.get_template("createProfile/editProfiles.html")
    return HttpResponse(template.render({'contacts': db['contacts']}))

@csrf_exempt
def getKeywords(request):
    global inConvo
    dirpath = os.path.dirname(os.path.realpath(__file__))
    with open(dirpath + '/db.json') as src:
        db = json.load(src)
        print(db)
    if request.method == 'POST':
        if len(request.FILES):
            fileObj = request.FILES['filee']
            text = speechToText.main(fileObj)
            print("inConvo", inConvo)
            if text != "":
                if inConvo:
                    # look for end phrases assume a convo exists so just append to end of convos
                    if len(db['convos']) == 0:
                        inConvo = False
                    else:
                        db['convos'][-1]['text'] = db['convos'][-1]['text'] + " " + text
                        for phrase in end_trigger_phrases:
                            if phrase in text:
                                # trigger end of convo
                                ts = time.time()
                                db['convos'][-1]['endTime'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                                inConvo = False
                else:
                    # looking for start trigger phrase
                    for phrase in start_trigger_phrases:
                        if phrase in text:
                            inConvo = True
                            ts = time.time()
                            startTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                            db['convos'].append({
                                'text': text,
                                'startTime': startTime,
                                'endTime': None
                            })
        else:
            print("no file")
        with open(dirpath + '/db.json', 'w+') as outfile:
            json.dump(db, outfile)
    return HttpResponse(db)
