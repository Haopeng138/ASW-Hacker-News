from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
import requests

def getTopIds():
  respon = requests.get(url="https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
  return respon.json()

def getTop30():
  topIds = getTopIds()
  idlist = []
  for index,id  in enumerate(topIds,start=1):
      if index == 31:
          break
      idlist.append(id)
  return idlist


def index(request):
  context ={}
  template = loader.get_template('homepage.html')
  topIds = getTopIds
  return HttpResponse(template.render(context,request))

def submit(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render(None, request))

@csrf_exempt
def create(request):
  usr = request.POST['acct']
  pwd = request.POST['pw']
  newUser = Login(username=usr, password = pwd)
  newUser.save()
  output = "Create Usr: " + usr + " Pw: " + pwd
  print(output)
  return HttpResponse(testIndex(request))


def login(request):
  usr = request.POST['acct']
  pwd = request.POST['pw']

  output = "Usr: " + usr + " Pw: " + pwd
  print(output)
  return HttpResponse(output,request)


def testIndex(request):
  myusers = Login.objects.all().values()
  template = loader.get_template('testUsr.html')
  context = { 'myusers' : myusers, }
  return HttpResponse(template.render(context, request))

