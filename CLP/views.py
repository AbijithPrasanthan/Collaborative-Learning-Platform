from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    d = {
        'insert_me': 'This is the view.py file'
    }
    return render(request, 'CLP/index.html', context=d)

def login(request):
    return render(request, 'CLP/login.html')