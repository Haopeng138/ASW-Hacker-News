import allauth.account.auth_backends
import django.contrib.auth
from django.contrib import messages
from django.contrib.auth import get_user_model, authenticate, login
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import HNUser
from .adapters import HN_AccountAdapter

# Create your views here.

def account(request):
    userModel = get_user_model()
    succesful_login_url='/homepage'
    tempalte_name = 'testLogin.html'

    if request.POST.get('submit')=='Sign Up':
        print("Sign up")

        username=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('pw')

        if userModel.objects.filter(email=email).exists():
            messages.warning(request,'Email already exists')

        else:
            user = userModel.objects.create_user(email=email,password=password,username=username)
            user.set_password(password)
            user.save()
            messages.success(request,'User has been registered successfully')      #Dispalys message that user has been registerd
            HN_AccountAdapter.login(self=HN_AccountAdapter, request=request, user=user)
            return redirect(succesful_login_url)

    elif request.POST.get('submit')=='Log in':
        print("Login")

        email = request.POST['email']
        password = request.POST['pw']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            print("Autheticated user: " + user.get_username())
            HN_AccountAdapter.login(self=HN_AccountAdapter,request=request, user=user)
            return redirect (succesful_login_url)
        else:
            messages.warning(request,'Invalid credentials')

    return render(request,template_name=tempalte_name)

def logout(request):
    if request.user.is_authenticated:
        django.contrib.auth.logout(request)
        return redirect('/homepage')
    return redirect('/account')

