import django.contrib.auth
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
import requests
from django.contrib.auth import get_user_model, authenticate


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


def account(request):
  # return redirect('/account/',permanent=True)
  userModel = get_user_model()
  print("He llegado aqui")
  #userModel = hackersNews.accounts.models.HNUser
  if request.POST.get('submit')=='Sign Up':
    print("Sign up")
    username=request.POST.get('username')
    email=request.POST.get('email')
    password=request.POST.get('pw')

    if userModel.objects.filter(email=email).exists():                             # Condition for same email id if already exists
      messages.warning(request,'Email already exists')
    else:
      user =userModel.objects.create_user(email=email,password=password,username=username)
      user.set_password(password)                                             #since raw passwords are not saved therefore needs to set in this method
      user.save()
      messages.success(request,'User has been registered successfully')      #Dispalys message that user has been registerd
      django.contrib.auth.login(request, user)
    return redirect('/homepage/account')

  elif request.POST.get('submit')=='Log in':
    print("Login")
    email = request.POST['email']
    password = request.POST['pw']

    user = authenticate(request, email=email, password=password)
    print(user)
    if user is not None:
      django.contrib.auth.login(request, user)
      return redirect ('/')
    else:
      messages.warning(request,'Invalid credentials')
  # print(email,password,username)

  return render(request,'testLogin.html')

