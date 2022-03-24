from django.shortcuts import render, HttpResponse

def index(request):
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