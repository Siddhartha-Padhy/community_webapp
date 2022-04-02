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
    if request.user.is_authenticated:
        username = request.user.username
    data = {
        'active': 'explore',
        'username': username,
    }
    
    return render(request, 'explore.html', data)

def search_results(request,value):
    value = ' '.join(value.split())
    users = User.objects.filter(first_name__contains=value)
    results = []
    for user in users.iterator():
        result = {}
        result['username'] = str(user.get_username())
        result['profileName'] = str(user.get_short_name())
        results.append(result)

    data = {
        'results': results
    }
    return JsonResponse(data)

@login_required
def explore_profile(request,value):
    if request.user.is_authenticated:
        username = request.user.username

    user = User.objects.get(username=value)
    profile_name = user.get_short_name()
    status = get_personal_status(user.get_username())
    posts = get_personal_posts(value)
    data = {
        'active': 'explore',
        'username': username,
        'profile_username': user.get_username(),
        'profile_name': profile_name,
        'status': status,
        'posts': posts
    }
    return render(request, 'profile.html', data)

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
    status = get_personal_status(username)
    posts = get_personal_posts(username)
    data = {
        'active': 'profile',
        'username': username,
        'profile_username': username,
        'profile_name': profile_name,
        'status': status,
        'posts': posts
    }
    return render(request, 'profile.html', data)

@login_required
@csrf_exempt
def edit_profile(request):
    error = None
    username = request.user.username
    if request.method == "POST":
        profileName = str(request.POST.get('profileName'))
        email = str(request.POST.get('email'))
        status = str(request.POST.get('status'))
        try:
            user = User.objects.get(username = username)
            user.first_name = profileName
            user.email = email
            user.save()
            set_status(username,status)
        except Exception as e:
            print('Error: ' + str(e))
            error = 'Something went Wrong!'
    data = {
        'active': 'profile',
        'username': username,
        'error': error
    }
    return render(request, 'edit_profile.html', data)

@login_required
def about(request):
    if request.user.is_authenticated:
        username = request.user.username
    data = {
        'active': 'about',
        'username': username
    }
    return render(request, 'about.html', data)