from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=40,null = True)
class Driver(models.Model):
    drivername = models.CharField(max_length=20)
    vehicle_type = models.CharField(max_length=20)
    license_number = models.IntegerField(default=0)
    capacity = models.IntegerField(default=0)
    other_info = models.CharField(max_length=80)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,       
        null = True,
    )
    
class Ride(models.Model):
    # the state of the ride can be: open/confirmed/closed/complete
    state = models.CharField(max_length=10)
    # id of the ride owner: default 0, cannot be 0
    # !! should be dynamically allocated as the owner goes away
    driver = models.ForeignKey(
        Driver,
        on_delete = models.SET_NULL,
        null = True,
    )
    # id(s) of the ride sharer(s):
    #   appended to the existing string's tail in time order
    #   when owner goes away, the leading sharer will automatically become the new owner#
    # required arrival datetime, can only be set/edited by owner
    arrival_datetime = models.DateTimeField()
    # destination, cannot be null, can only be set/edited by owner
    destination = models.CharField(max_length = 100)
    # this ride can be shared: cannot be null, can only be set/edited by owner
    # Boolean: True or False
    can_share = models.BooleanField(default = True)
    # person number list: 10 slots, first slot for owner, 1-1 relationship sharer
    # total person number: the sum of person number list
    total_rider_number = models.IntegerField(default=0)
    # other info: a string, can only be set/edited by owner
    # matching: strictly
    # !! optional
    other_info = models.CharField(max_length=200)
    # required vehicle type, can only be set/edited by sharer
    # matching: strictly
    # !! optional
    required_vehicle_type = models.CharField(max_length=200)
    

class Personal_ride(models.Model):
    user = models.ForeignKey(
        User,
        on_delete = models.CASCADE,
    )
    ride = models.ForeignKey(
        Ride,
        on_delete = models.CASCADE,
        null = True,
    )
    called_time = models.DateTimeField()
    identity = models.CharField(max_length=20)
    party_person_number = models.IntegerField(default = 0)
    
