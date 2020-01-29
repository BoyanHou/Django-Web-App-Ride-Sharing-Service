from django.shortcuts import render
from .models import User
from .models import Ride
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Driver #import the class here

def register_process(request):
    user = User(username=request.POST['username'], password=request.POST['password'])
    user.save()
    return HttpResponseRedirect(reverse('uper:index')) # use reverse() to avoid hard-code url

def login(request):
    if request.method == 'POST':
        username_ = request.POST['username']
        password_ = request.POST['password']
        exist = User.objects.filter(username = username_, password = password_)
        
        if exist: # on successful login
            # set session cookie
            user_id = User.objects.get(username = username_).id
            request.session["user_id"] = user_id 
            # redirect to Uper main page
            return HttpResponseRedirect(reverse('uper:main_page'))            

        else: # fail to login
            return HttpResponse('Wrong username or password!')

def main_page(request):
    # get current user id from session
    user_id = request.session["user_id"]
    username = User.objects.get(pk = user_id).username

    # build the ride list as owner, driver, and sharer
    ride_list_as_owner =  Ride.objects.filter(owner_id = user_id)
#    ride_list_as_sharer = Ride.objects.filter(sharer_id_list__contains() = [user_id])
    ride_list_as_driver = Ride.objects.filter(driver_id = user_id)
    
    
    # build context dictionary to inject into html page
    context = {'username':username,
               'ride_list_as_owner':ride_list_as_owner,
    }
    return render(request, 'uper/main_page.html', context)


def request_ride_process(request):
    # collect ride info:
    # set: state as "open"
    state = "open"
    # session: owner id, get current user id from session
    owner_id = request.session["user_id"]
    if not owner_id: # the user is not logged in
        return HttpResponse("Please log in first!") # warning
    # skip:sharer id array is empty by default
    # skip:driver id is empty by defualt
    # form: arrival datetime
    arrival_datetime = request.POST["arrival_datetime"]
    if not arrival_datetime: # this input field is a must
        return HttpResponse("Please enter your required arrival date and time!") # warning
    # form: destination
    destination = request.POST["destination"]
    if not destination: # this input field is a must
        return HttpResponse("Please enter your destination") # warning
    # form: can share by sharers
    can_share = request.POST["can_share"]
    if not can_share: # this input field is a must
        return HttpResponse("Please tell us if you want to share this ride!") # warning
    # form: total number of the owner's group
    owner_party_person_number = request.POST["owner_party_person_number"]
    if not owner_party_person_number: # this input field is a must
        return HttpResponse("Please tell us how many people are in your party!") # warning
    # make the 10-slot person_number_list, owner number occupies the first slot
    person_number_list = [owner_party_person_number,
                          0,0,0,
                          0,0,0,
                          0,0,0,
    ]
    # set total person number = owner party person number
    total_person_number = owner_party_person_number
    # form: other info (optional)
    other_info = request.POST["other_info"]
    # form: required vehicle type (optional)
    required_vehicle_type = request.POST["required_vehicle_type"]

    # create object
    ride = Ride(state = state,
                owner_id = owner_id,
                # skip sharer id list--default as null 
                driver_id = 0, # skip driver id
                arrival_datetime = arrival_datetime,
                destination = destination,
                can_share = can_share,
                person_number_list = person_number_list,
                total_person_number = total_person_number,
                other_info = other_info,
                required_vehicle_type = required_vehicle_type,
    )
    
    # save this requested ride into database
    ride.save()
    # redirect back into main page
    return HttpResponseRedirect(reverse('uper:main_page'));

def view_info(request):
    user_id = request.session["user_id"]
    username = User.objects.get(pk = user_id).username
    drivername = Driver.objects.get(user_id = user_id).drivername
    vehicle_type = Driver.objects.get(user_id = user_id).vehicle_type
    license_number = Driver.objects.get(user_id = user_id).license_number
    capacity = Driver.objects.get(user_id = user_id).capacity
    other_info = Driver.objects.get(user_id = user_id).other_info
    if(Driver.objects.filter(user_id = user_id)):
        context = {'user_id':user_id, 'username':username, 'drivername':drivername, 'vehicle_type':vehicle_type, 'license_number':license_number, 'capacity':capacity, 'other_info':other_info,}
    return render(request, 'uper/view_info.html', context)

def logout(request):
    #delete session id and logout
     if request.method == 'POST':
         del request.session['user_id']
         return HttpResponseRedirect(reverse('uper:index'))            

def driver_reg(request):
    #register information for driver
    drivername = request.POST['drivername']
    vehicle_type = request.POST['vehicle_type']
    license_number = request.POST['license_number']
    capacity = request.POST['capacity']
    other_info = request.POST['other_info']
    user_id = request.session['user_id']
    #return error page if the the input except other_info is empty
    if not drivername or not vehicle_type or not license_number or not capacity:
        return HttpResponse("Your input is not valid!")
    else:
        driver = Driver(drivername=drivername, vehicle_type=vehicle_type, license_number=license_number, capacity=capacity,other_info=other_info,user_id=user_id)
        driver.save()
        return HttpResponseRedirect(reverse('uper:main_page'))
        

