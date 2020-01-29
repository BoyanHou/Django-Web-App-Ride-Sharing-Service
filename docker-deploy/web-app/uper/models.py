from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)


class Ride(models.Model):
    # the state of the ride can be: open/confirmed/closed/complete
    state = models.CharField(max_length=10)
    # id of the ride owner: default 0, cannot be 0
    # !! should be dynamically allocated as the owner goes away
    owner_id = models.IntegerField(default=0)
    # id(s) of the ride sharer(s):
    #   appended to the existing string's tail in time order
    #   when owner goes away, the leading sharer will automatically become the new owner
    #   can be empty
    #   max 9 sharers
    sharer_id_list = ArrayField(
        models.IntegerField(default=0),
        size = 9,
        null = True,
    )
    # driver id, can be 0, indicating no driver has picked up this ride yet
    driver_id = models.IntegerField(default=0)
    # required arrival datetime, can only be set/edited by owner
    arrival_datetime = models.DateTimeField()
    # destination, cannot be null, can only be set/edited by owner
    destination = models.CharField(max_length = 100)
    # this ride can be shared: cannot be null, can only be set/edited by owner
    # yes or no
    can_share = models.CharField(max_length = 10)
    # person number list: 10 slots, first slot for owner, 1-1 relationship sharer
    person_number_list = ArrayField(
        models.IntegerField(default=0),
        size = 10,
        null = True, # default is null
    )
    # total person number: the sum of person number list
    # default 0; cannot be 0 -- if 0, then close this ride
    total_person_number = models.IntegerField(default=0)
    # other info: a string, can only be set/edited by owner
    # matching: strictly
    # !! optional
    other_info = models.CharField(max_length=200)
    # required vehicle type, can only be set/edited by sharer
    # matching: strictly
    # !! optional
    required_vehicle_type = models.CharField(max_length=200)

    
class Driver(models.Model):
    drivername = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)
    license_number = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    other_info = models.CharField(max_length=80)
    #use user id to connect driver account with user account
    user_id = models.IntegerField(default=0)

