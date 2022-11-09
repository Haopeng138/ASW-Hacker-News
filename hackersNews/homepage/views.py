import django.contrib.auth
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
from .models import *
import requests
from urllib.parse import urlparse
import math
import datetime
from .models import Post
from django.contrib.auth import get_user_model, authenticate
from accounts.models import HNUser
from django.core.validators import validate_email
from django.core.mail import send_mail
## Pagina principal 
def index(request,page=None):
  template = loader.get_template('index.html')
  posts = Post.objects.all()
  context = {
     'post' : posts
  }
  return HttpResponse(template.render(None,request))

## Login,  ¿borrar ? 
def submit(request):
  template = loader.get_template('registration/login.html')
  return HttpResponse(template.render(None,request))



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

def logout(request):
  
  return redirect('/')


def testIndex(request):
  myusers = Login.objects.all().values()
  template = loader.get_template('testUsr.html')
  context = { 'myusers' : myusers, }
  return HttpResponse(template.render(context, request))


def account(request):
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


# def testProfile(request):
#   template = loader.get_template('user/profile.html')
#   context = {
#     'username': 'hao',
#     'karma': 3, 
#     'email': 'hao@gmail.com',
#     'about': 'Mucho texto',
#     'own_user': True
#   }
#   return HttpResponse(template.render(context, request))

def profile(request, user_id):
    #log.info(f'Loading profile {user_id}...')
    user_query = HNUser.objects.filter(id=user_id)

    if user_query:
        user = user_query[0]

        if user.id == request.user.id:
            context = {
                'user_id': user_id,
                'username': user.username,
                'karma': user.karma,
                'about': user.about,
                'email': user.email,
                'own_user': True
            }
        else:
            context = {
                'user_id': user_id,
                'username': user.username,
                'karma': user.karma,
                'about': user.about,
                'own_user': False
            }
        return render(request, 'user/profile.html', context=context)
    else:
        return redirect('index')

def validate_user_email(email):
    try:
        validate_email(email)
        return True
    except :
        
        return False

def send_confirmation_email(user):
    confirmation_email_text = f"""Hi {user.username},\n\nHo"""
    send_mail(
        subject=f'Confirmation email from Hacker Newst',
        message=confirmation_email_text,
        from_email='info@datatau.net',
        recipient_list=[user.email],
        fail_silently=False
    )

def update_profile(request, user_id):
    if request.method == 'POST':
        body = request.POST

        updated_profile = False

        user = request.user
        if 'about' in body:
            user.about = body['about']
            updated_profile = True

        invalid_email = True
        if 'email' in body and validate_user_email(body['email']):
            user.email = body['email']
            #user.is_active = False

            user.save()

            #send_confirmation_email(user)

            #return HttpResponse(
                #"<h1>Email successfully updated!</h1><p>We've just sent you a confirmation email. Please check your inbox and click on the confirmation link :)</p>")

        user.save()

  

        context = {
            'user_id': user_id,
            'username': user.username,
            'karma': user.karma,
            'about': user.about,
            'email': user.email,
            'invalid_email': invalid_email,
            'updated_profile': updated_profile,
            'own_user': True
        }
        return render(request, 'user/profile.html', context=context)

def testPost(request):
  current_post ={
    'title': "Titulo random",
    'id': 45342,
    'user': {
      'username':'hao',
      'id': 3,
    },
    'url': "some@gmail.com",
    'side': 'www.google.com',
    'votes':4,
    'time_from_post': 1341,

  }

  posttracking = [
    45352
  ]
  context = {'post': current_post,
            'post_tracking': posttracking,
            'tracking': 3243,
            'root_comments': 4324,
            'error': True}
  return render(request,'post/post.html',context)

def testSubmitPost(request):
  context = {
    'error':False
  }
  return render(request,'post/submit.html',context)

def testPostEdit(request):
  current_post ={
  'title': "Titulo random",
  'id': 45342,
  'user': {
    'username':'hao',
    'id': 3,
  },
  'url': "some@gmail.com",
  'site': 'www.google.com',
  'votes':4,
  'time_from_post': 1341,
  }
  context = {
    'post':current_post,
    
  }
  return render(request,'post/post_edit.html',context)