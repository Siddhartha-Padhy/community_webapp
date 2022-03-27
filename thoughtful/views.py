from time import sleep
from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

def login(request):
    return render(request,'login.html')

def home(request):
    username = 'peter_parker'
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

def profile(request):
    data = {
        'active': 'profile',
        'username': 'peter_parker'
    }
    return render(request, 'profile.html', data)

def about(request):
    data = {
        'active': 'about',
        'username': 'peter_parker'
    }
    return render(request, 'about.html', data)