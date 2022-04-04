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

# Home page for logged in user
@login_required
def home(request):
    username = ''
    if request.user.is_authenticated:
        username = request.user.username

    posts = get_posts_by_followings(username)
    data = {
        'active': 'home',
        'username': username,
        'posts': posts
    }
    
    return render(request, 'home.html', data)

# Page for composing posts
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

# Explore users
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

# Sends JSON respose for found users with queried first_name
# Loads in Explore page without page reload
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

# Profile page for other users using the profile template
@login_required
def explore_profile(request,value):
    if request.user.is_authenticated:
        username = request.user.username

    user = User.objects.get(username=value)
    profile_name = user.get_short_name()
    status = get_status(user.get_username())
    posts = get_posts(value)
    following = get_following(user.get_username())
    data = {
        'active': 'explore',
        'username': username,
        'profile_username': user.get_username(),
        'profile_name': profile_name,
        'status': status,
        'following': following,
        'posts': posts
    }
    return render(request, 'profile.html', data)

# Notification page
@login_required
def notification(request):
    data = {
        'active': 'notification',
        'username': 'peter_parker'
    }
    return render(request, 'notification.html', data)

# Profile page for logged in user
@login_required
def profile(request):
    if request.user.is_authenticated:
        username = request.user.username
        profile_name = request.user.first_name
    status = get_status(username)
    posts = get_posts(username)
    following = get_following(username)
    data = {
        'active': 'profile',
        'username': username,
        'profile_username': username,
        'profile_name': profile_name,
        'status': status,
        'following': following,
        'posts': posts
    }
    return render(request, 'profile.html', data)

# Adds a user to logged in user's following list
@login_required
def follow_profile(request,value):
    print(value)
    follow_user(request.user.username,value)
    data = {
        'results': 'success'
    }
    return JsonResponse(data)

# Form page to update logged in user's data
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

# About page
@login_required
def about(request):
    if request.user.is_authenticated:
        username = request.user.username
    data = {
        'active': 'about',
        'username': username
    }
    return render(request, 'about.html', data)