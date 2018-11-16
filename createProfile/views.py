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
convo = None
occupation_types = [
    "engineer", "artist", "designer", "actor", "architecture", "sales", "baker","musician",
    "lawyer", "doctor", "dancer", "manager", "recruiter", "banker", "accountant", "consultant", "teacher",
    "reporter", "professor", "student"]
company_names = [
    "facebook", "airbnb", "google", "microsoft", "amazon", "apple", "salesforce"
]
names = [
    "kristin", "kristen", "christine", "kevin", "stephanie", "tina", "christina", "ken", "jason", "selena", "chris", "andrew", "dan", "jeff", "katherine"
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
def in_progress(request):
    template = loader.get_template("createProfile/in_progress.html")
    return HttpResponse(template.render())

@csrf_exempt
def index(request):
    template = loader.get_template("createProfile/index.html")
    return HttpResponse(template.render())


def createContacts():
    dirpath = os.path.dirname(os.path.realpath(__file__))
    with open(dirpath + '/db.json') as src:
        db = json.load(src)
    result = []
    for convo in db['convos']:

        keywords = parser.main(convo['text'])
        name = ""
        occupation = ""
        company = ""
        home = ""
        keyPoints = []
        saliences = []
        for word in keywords:
            if occupation == "" and word['name'].lower() != yourOccupation and isOccupation(word['name'].lower()):
                print("set occupation", word['name'])
                occupation = word['name']
            elif company == "" and word['name'].lower() != yourCompany and word['name'].lower() in company_names:
                company = word['name']
            elif name == "" and word['type'] == 'PERSON' and word['name'].lower() != yourName and word['name'].lower() in names:
                name = word['name']
            elif home == "" and word['type'] == 'LOCATION' and word['name'].lower() != yourHome:
                home = word['name']
            else:
                keyPoints.append(word['name'])
                saliences.append(word['salience'])

        newContact = {
            'name': name,
            'occupation': occupation,
            'home': home,
            'company': company,
            'keywords': keyPoints,
            'saliences': saliences,
            'uniqWords': list(set(keyPoints)),
            'startTime': convo['startTime'],
            'endTime': convo['endTime']
        }

        result.append(newContact)

    db['contacts'] += result
    db['convos'] = []
    with open(dirpath + '/db.json', 'w+') as outfile:
        json.dump(db, outfile)
    return db['contacts']
    # return result


@csrf_exempt
def getKeywords(request):
    global inConvo, convo
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
                    convo['text'] = convo['text'] + " " + text
                    for phrase in end_trigger_phrases:
                        if phrase in text:
                            # trigger end of convo
                            ts = time.time()
                            convo['endTime'] = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                            db['convos'].append(convo)
                            inConvo = False
                            with open(dirpath + '/db.json', 'w+') as outfile:
                                json.dump(db, outfile)
                            break
                else:
                    # looking for start trigger phrase
                    for phrase in start_trigger_phrases:
                        if phrase in text:
                            inConvo = True
                            ts = time.time()
                            startTime = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
                            convo = {
                                'text': text,
                                'startTime': startTime,
                                'endTime': None
                            }
        else:
            print("no file")

    return HttpResponse(db)

@csrf_exempt
def summary(request):
    newContacts = createContacts()
    template = loader.get_template("createProfile/event_summary.html")
    return HttpResponse(template.render({"contacts": newContacts}))
@csrf_exempt
def viewProfile(request):
    result = None
    if request.method == "POST":
        if "contactName" in request.POST:
            ourName = request.POST["contactName"]
            print(ourName)
            dirpath = os.path.dirname(os.path.realpath(__file__))
            with open(dirpath + '/db.json') as src:
                db = json.load(src)
            for contact in db["contacts"]:
                if contact["name"] == ourName:
                    print(contact)
                    result = contact
    template = loader.get_template("createProfile/viewProfile.html")
    return HttpResponse(template.render({"contact": result}))
