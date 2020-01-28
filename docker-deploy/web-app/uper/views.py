from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import User

def index(request):
#    return HttpResponse("Uper is Awesome!")
    return render(request, 'uper/index.html')

def register(request):
    return HttpResponse("Register Page");

def login(request):
    return HttpResponse("Login Logic TBD");
