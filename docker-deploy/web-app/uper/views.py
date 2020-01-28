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
    if request.method == 'POST':
        username_ = request.POST.get('username_')
        password_ = request.POST.get('password_')
        exist = User.objects.filter(username = username_, password = password_)
        if exist:
            return HttpResponse('login successfully!')           
        else:
            return HttpResponse('Wrong username or password!')
        

