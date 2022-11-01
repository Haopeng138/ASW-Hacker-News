from django.http import HttpResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import Login
import requests
from urllib.parse import urlparse
import math
import datetime
from .models import Post

def index(request,page=None):
  template = loader.get_template('index.html')
  posts = Post.objects.all()
  context = {
     'post' : posts
  }
  return HttpResponse(template.render())

def submit(request):
  template = loader.get_template('login.html')
  return HttpResponse(template.render())

@csrf_exempt
def create(request):
  usr = request.POST['acct']
  pwd = request.POST['pw']
  newUser = Login(username=usr, password = pwd)
  newUser.save()
  output = "Create Usr: " + usr + " Pw: " + pwd
  print(output)
  return HttpResponse(testIndex(request))

@csrf_exempt
def login(request):
  usr = request.POST['acct']
  pwd = request.POST['pw']

  output = "Usr: " + usr + " Pw: " + pwd
  print(output)
  return HttpResponse(output)


def testIndex(request):
  myusers = Login.objects.all().values()
  template = loader.get_template('testUsr.html')
  context = { 'myusers' : myusers, }
  return HttpResponse(template.render(context, request))
