from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from datetime import * #to compare date
import datetime
from .models import User, Driver, Ride, Personal_ride


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
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");
    
    # get current user id from session
    user_id = request.session["user_id"]
    user = User.objects.get(pk = user_id)
    username = user.username

    # build the ride list as owner, driver, and sharer
    personal_ride_list_as_owner = user.personal_ride_set.filter(identity = "owner")
    personal_ride_list_as_sharer = user.personal_ride_set.filter(identity = "sharer")
    personal_ride_list_as_driver = user.personal_ride_set.filter(identity = "driver")
    personal_ride_lists = {'personal_ride_list_as_owner':
                           {'identity':"owner",
                            'list':personal_ride_list_as_owner},
                           'personal_ride_list_as_sharer':
                           {'identity':"sharer",
                            'list':personal_ride_list_as_sharer},
                           'personal_ride_list_as_driver':
                           {'identity':"driver",
                            list:personal_ride_list_as_driver},
    }
    
    # build context dictionary to inject into html page
    context = {'username':username,
               'personal_ride_lists':personal_ride_lists,
    }
    
    return render(request, 'uper/main_page.html', context)

def request_ride(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");
    checklist = {"arrival_datetime":"arrival date and time",
                 "destination":"destination",
                 "can_share":"intention to share this ride or not",
                 "party_person_number":"person number in your party",
    }

    context = {'party_person_number_range':range(1, 10),
               'operation':"request",
               'checklist':checklist,
    }
    
    return render(request, 'uper/request_or_edit_ride.html', context)

def edit_ride(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");
    # sticky form: get the existing ride and personal ride objects from DB
    personal_ride = Personal_ride.objects.get(pk = request.POST['personal_ride_id'])
    ride = personal_ride.ride
    if ride.can_share:
        can_share = "yes"
    else:
        can_share = "no"
    if personal_ride.identity == "driver":
        ride.delete()
        return HttpRequestRedirect(reverse('uper:main_page'))
    else:
        checklist = ["arrival_datetime",
                 "destination",
                 "can_share",
                 "party_person_number",
        ]
        context = {'party_person_number_range':range(1, 10),
                   'personal_ride':personal_ride,
                   'ride':ride,
                   'operation':"edit",
                   'can_share':can_share,
                   'check_list':checklist,
        }
        return render(request, 'uper/request_or_edit_ride.html', context)

def request_or_edit_ride_process(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");
    
    # Find the user object from DB
    user_id = request.session["user_id"]
    if not user_id: # the user is not logged in
        return HttpResponse("Please log in first!") # warning
    user = User.objects.get(pk = user_id)

    if request.POST["operation"] == "request":
    # Create a new personal_ride
        personal_ride = Personal_ride(
            user = user,
            called_time = datetime.datetime.now(),
            identity = "owner",
            party_person_number = request.POST["party_person_number"],
        )    
    else:
    # Edit an existing personal_ride 
        personal_ride = Personal_ride.objects.get(pk = request.POST.get('personal_ride_id'))
        # record previous person number in party, for new total person number calculation
        previous_party_person_number = personal_ride.party_person_number
        personal_ride.party_person_number = request.POST["party_person_number"]

    personal_ride.save()

    # Extract form data
    arrival_datetime = request.POST["arrival_datetime"]
    if not arrival_datetime: # this input field is a must
        return HttpResponse("Please enter your required arrival date and time!") # warning
    destination = request.POST["destination"]
    if not destination: # this input field is a must
        return HttpResponse("Please enter your destination") # warning
    can_share_str = request.POST["can_share"]
    if not can_share_str: # this input field is a must
        return HttpResponse("Please tell us if you want to share this ride!") # warning
    if can_share_str == "yes":
        can_share = True
    else:
        can_share = False    
    other_info = request.POST["other_info"]
    required_vehicle_type = request.POST["required_vehicle_type"]

    if request.POST["operation"] == "request":
    # Create a ride containing this personal ride
        ride = Ride(state = "open",
                    # no driver yet
                    arrival_datetime = arrival_datetime,
                    destination = destination,
                    can_share = can_share,
                    total_rider_number = request.POST["party_person_number"],
                    other_info = other_info,
                    required_vehicle_type = required_vehicle_type,
        )
        ride.save()
        # add owner's personal ride into this ride
        ride.personal_ride_set.add(personal_ride)
    else:
    # edit an existing ride
        ride = personal_ride.ride
        ride.arrival_datetime = arrival_datetime
        ride.destination = destination
        ride.can_share = can_share
        ride.total_rider_number = ride.total_rider_number-previous_party_person_number+int(request.POST["party_person_number"])
        ride.other_info = other_info
        ride.required_vehicle_type = required_vehicle_type
        ride.save()
        
    # redirect back into main page
    return HttpResponseRedirect(reverse('uper:main_page'))

def view_info(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");
    
    user_id = request.session["user_id"]
    user = User.objects.get(pk = user_id)
    username = user.username
    if(hasattr(user,'driver')):
        Driver_ = user.driver
    else:
        Driver_ = None
    if(Driver_):
        #result of filter is a set, get the first set
        context = {'user_id':user_id,'username':username,'Driver_':Driver_,}
    else:
        #if the Driver_ is not found, add empty as the value in driver
        context = {'user_id':user_id,'username':username,'Driver_':Driver_,}
    return render(request, 'uper/view_info.html', context)

def logout(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");

    #delete session id and logout
    if request.method == 'POST':
        del request.session['user_id']
        return HttpResponseRedirect(reverse('uper:index'))            

def driver_reg(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");

    # get user login info
    user_id = request.session['user_id']
    user = User.objects.get(pk = user_id)
    
    if hasattr(user, 'driver'):
        return  HttpResponse("You have already registered as a driver!")
    else:
        return render(request, 'uper/driver_register.html');
     
def driver_reg_process(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");

    # get user login info
    user_id = request.session['user_id']
    user = User.objects.get(pk = user_id)  
    
    #register information for driver
    drivername = request.POST['drivername']
    vehicle_type = request.POST['vehicle_type']
    license_number = request.POST['license_number']
    capacity = request.POST['capacity']
    other_info = request.POST['other_info']
   
    #return error page if the the input except other_info is empty
    if not drivername: 
        return HttpResponse("Please tell us your name!")
    if not vehicle_type:
        return HttpResponse("Please tell us your vehicle type!")
    if not license_number:
        return HttpResponse("Please tell us your license number!")
    if not capacity:
        return HttpResponse("Please tell us the capacity of your vehicle!")
    driver = Driver(drivername=drivername,
                    vehicle_type=vehicle_type,
                    license_number=license_number,
                    capacity=capacity,
                    other_info=other_info,
                    user = user,
    )
    driver.save()
    return HttpResponseRedirect(reverse('uper:main_page'))
        

def edit_driver(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");

    # get login info
    user_id = request.session["user_id"]
    user = User.objects.get(pk = user_id)

    #edit the personal/vehicle info and driver status
    driver= user.driver
    drivername = request.POST['drivername']
    vehicle_type = request.POST['vehicle_type']
    license_number = request.POST['license_number']
    capacity = request.POST['capacity']
    other_info = request.POST['other_info']
    if not driver:
        return HttpResponse("Driver doesn't exist!")
    if(drivername):
        driver.drivername = drivername
    if(vehicle_type):
        driver.vehicle_type = vehicle_type
    if(license_number):
        driver.license_number = license_number
    if(capacity):
        driver.capacity = capacity
    if(other_info):
        driver.other_info = other_info
    driver.save()
    return HttpResponseRedirect(reverse('uper:main_page'))

def shareride_search_result(request):
    if not login_status_is_valid(request):
        return HttpResponse("Please Login First!");
    
    # get user login info
    user_id = request.session["user_id"]
    user = User.objects.get(pk = user_id)

    # read html form
    passenger_number = int(request.POST['passenger_number'])
    destination = request.POST['destination']
    arrival_earliest = request.POST['arrival_earliest']
    arrival_latest = request.POST['arrival_latest']
#    print(arrival_ealiest)
    #the number of passenger should be valid number
    if(passenger_number <= 0):
        return HttpResponse("Your passenger_number is invalid",)
    #search for open rides that match our requirment
    ride_list_found = Ride.objects.filter(destination = destination , arrival_datetime__lte = arrival_latest,can_share = True,).filter(arrival_datetime__gte = arrival_earliest,state= "open")
    if(ride_list_found):
        context = {'ride_list_found':ride_list_found,'sharer_number':passenger_number,}
        return render(request,'uper/shareride_search_result.html',context)
    return HttpResponse("No ride is found")

def join_shareride(request):
    ride_id = request.POST["ride_id"]
    sharer_num =  int(request.POST["sharer_num"])
    ride = Ride.objects.get(pk=ride_id)
    ride.total_rider_number += sharer_num
    ride.save()
    return HttpResponseRedirect(reverse('uper:main_page'))

def driver_ride_search(request):
    user_id = request.session["user_id"]
    user = User.objects.get(pk = user_id)
    capacity = user.driver.capacity
    other_info = user.driver.other_info
    vehicle_type = user.driver.vehicle_type
    driver_ride_list_found = Ride.objects.filter(state="open",total_rider_number__lte=capacity, other_info = other_info, required_vehicle_type = vehicle_type)
    if(driver_ride_list_found):
        context = {'driver_ride_list_found':driver_ride_list_found,'driver_id':user_id}
        return render(request,'uper/driver_ride_list_found.html',context)
    return HttpResponse("No ride is found!")

def take_order(request):
    user_id = request.session["user_id"]
    user = User.objects.get(pk = user_id)
    ride = Ride.objects.get(pk = request.POST["ride_id"])
    user.driver.ride_set.add(ride);
    ride.state = "confirmed"
    return HttpResponseRedirect(reverse('uper:main_page'))
# Below are the common tool functions:
def login_status_is_valid(request):        
    user_id = request.session['user_id']
    exist = User.objects.get(pk = user_id)
    if not exist:
        return False
    else:
        return True    
    
    

    
        
        
