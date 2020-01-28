from django.shortcuts import render
from .models import User

# Create your views here.
from django.http import HttpResponse
from .models import User

def index(request):
    return render(request, 'uper/index.html')

def register_page(request):    
    return render(request, 'uper/register.html')

def register_process(request):
    user = User(username=request.POST['username'], password=request.POST['password'])
    user.save()
    return render(request, 'uper/index.html')

def login(request):
    return HttpResponse("Login Logic TBD")
