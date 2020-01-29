from django.shortcuts import render
from .models import User
from .models import Ride
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Driver #import the class here
from datetime import * #to compare date
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
    """
    drivername = Driver.objects.get(user_id = user_id).drivername
    vehicle_type = Driver.objects.get(user_id = user_id).vehicle_type
    license_number = Driver.objects.get(user_id = user_id).license_number
    capacity = Driver.objects.get(user_id = user_id).capacity
    other_info = Driver.objects.get(user_id = user_id).other_info
    """
    Driver_ = Driver.objects.filter(user_id = user_id)
    if(Driver_):
        #result of filter is a set, get the first set
        context = {'user_id':user_id,'username':username,'Driver_':Driver_[0],}
    else:
        #if the Driver_ is not found, add empty as the value in driver
        context = {'user_id':user_id,'username':username,'Driver_':Driver_,}
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
    if not drivername: 
        return HttpResponse("Please tell us your name!")
    if not vehicle_type:
        return HttpResponse("Please tell us your vehicle type!")
    if not license_number:
        return HttpResponse("Please tell us your license number!")
    if not capacity:
        return HttpResponse("Please tell us the capacity of your vehicle!")
    driver = Driver(drivername=drivername, vehicle_type=vehicle_type, license_number=license_number, capacity=capacity,other_info=other_info,user_id=user_id)
    driver.save()
    return HttpResponseRedirect(reverse('uper:main_page'))
        

def edit_driver(request):
    #edit the personal/vehicle info and driver status
    user_id = request.session["user_id"]
    Driver_list = Driver.objects.filter(user_id = user_id)
    drivername = request.POST['drivername']
    vehicle_type = request.POST['vehicle_type']
    license_number = request.POST['license_number']
    capacity = request.POST['capacity']
    other_info = request.POST['other_info']
    if not Driver_list:
        return HttpResponse("Driver doesn't exist!")
    Driver_ = Driver_list[0]
    if(drivername):
        Driver_.drivername = drivername
    if(vehicle_type):
        Driver_.vehicle_type = vehicle_type
    if(license_number):
        Driver_.license_number = license_number
    if(capacity):
        Driver_.capacity = capacity
    if(other_info):
        Driver_.other_info = other_info
    Driver_.save()
    return HttpResponseRedirect(reverse('uper:main_page'))

def shareride_search_result(request):
    user_id = request.session["user_id"]
    passenger_number = int(request.POST['passenger_number'])
    destination = request.POST['destination']
    arrival_earliest = request.POST['arrival_earliest']
    arrival_latest = request.POST['arrival_latest']
#    print(arrival_ealiest)
    #the number of passenger should be valid number
    if(passenger_number <= 0):
        return HttpResponse("Your passenger_number is invalid",)
    ride_list_found = Ride.objects.filter(destination = destination , arrival_datetime__lte = arrival_latest,can_share = "yes",).filter(arrival_datetime__gte = arrival_earliest,)
    if(ride_list_found):
        return HttpResponse("share ride")
    return HttpResponse("No ride is found")
    
