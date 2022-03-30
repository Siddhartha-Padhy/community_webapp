from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from thoughtful.database_functions import *
from django.http import JsonResponse

@csrf_exempt
def login(request):
    error = None
    if request.method == "POST":
        username = str(request.POST.get("username"))
        password = str(request.POST.get("password"))
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect(home)
            else:
                error = "Invalid Credentials"
        except Exception as e:
            print('Error: ',e)
            error = 'Something went wrong!'

    return render(request,'login.html',{'error': error})

@csrf_exempt
def signup(request):
    error = None
    if request.method == "POST":
        userEmail = str(request.POST.get("userEmail"))
        profileName = str(request.POST.get("profileName"))
        username = str(request.POST.get("username"))
        password = str(request.POST.get("password"))
        try:
            if validate_username(username):
                user = User.objects.create_user(username=username,email=userEmail,password=password,first_name=profileName)
                if user is not None:
                    create_user_database(username)
                    auth_login(request, user)
                    return redirect(home)
                else:
                    error = "Invalid Credentials"
            else:
                error = 'Username Exists'
        except Exception as e:
            print('Error: '+str(e))
            error = 'Something went wrong!'
    
    return render(request,'signup.html',{'error':error})

def logout(request):
    auth_logout(request)
    return redirect(login)

@login_required
def home(request):
    username = ''
    if request.user.is_authenticated:
        username = request.user.username
    posts = [
        {
        'author': 'Sandra',
        'date': '24/03/2022',
        'content': 'Lorem ipsum, dolor sit amet consectetur adipisicing elit. Sunt, a? Lorem ipsum dolor sit amet consectetur adipisicing elit. Maiores, vel?'
        },
        {
            'author': 'MaxAllen',
            'date': '23/03/2022',
            'content': 'Lorem ipsum dolor sit amet consectetur adipisicing elit. Itaque omnis adipisci quisquam eligendi neque harum minus iure ipsam deleniti rerum?'
        }
    ]
    data = {
        'active': 'home',
        'username': username,
        'posts': posts
    }
    
    return render(request, 'home.html', data)

@csrf_exempt
@login_required
def compose(request):
    error = None
    if request.method == "POST":
        content = str(request.POST.get('post-content'))
        try:
            make_post(request.user.username,content)
        except Exception as e:
            print('Error: ' + str(e))
            error = 'Something went Wrong!'
    data = {
        'active': 'compose',
        'username': 'peter_parker',
        'error': error
    }
    return render(request,'compose.html',data)

@login_required
@csrf_exempt
def explore(request):
    data = {
        'active': 'explore',
        'username': 'peter_parker',
    }
    if request.method == 'POST':
        print('request.form')
        # return ('',204)
        # return render(request, 'explore.html', data)
    
    return render(request, 'explore.html', data)

def search_results(request,id):
    data = {
        'results': [
        {
            'username': 'james_18',
            'name': 'James Clear'
        },
        {
            'username': 'nick_davidson',
            'name': 'Nick Davidson'
        },
        {
            'username': 'john_parkinson',
            'name': 'John Parkinson'
        }
    ]
    }
    return JsonResponse(data)

@login_required
def notification(request):
    data = {
        'active': 'notification',
        'username': 'peter_parker'
    }
    return render(request, 'notification.html', data)

@login_required
def profile(request):
    if request.user.is_authenticated:
        username = request.user.username
        profile_name = request.user.first_name
    data = {
        'active': 'profile',
        'username': username,
        'profile_name': profile_name
    }
    return render(request, 'profile.html', data)

@login_required
def about(request):
    data = {
        'active': 'about',
        'username': 'peter_parker'
    }
    return render(request, 'about.html', data)