from django.db import models

#Main Myhome models 
class MyHome(models.Model):
    name = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

#Room models in MyHome
class Room(models.Model):
    name = models.CharField(max_length=200)
    my_home = models.ForeignKey("myhome.MyHome",on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

#Channel models in Device
class Channel(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    room = models.ForeignKey("myhome.Room",on_delete=models.SET_NULL,null=True)
    #The State is for switch to on or off
    state = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

#Sensor models in room
class Sensor(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    device = models.ForeignKey("myhome.Device",on_delete=models.SET_NULL,null=True)
    room = models.ForeignKey("myhome.Room",on_delete=models.SET_NULL,null=True,related_name="sensor_room")
    # if sensor is temp, this value at persent
    state = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

#Product
class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    num_of_channels = models.IntegerField(default=1)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

#Device models in room
class Device(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    product = models.ForeignKey("myhome.Product",on_delete=models.SET_NULL,null=True)
    my_home = models.ForeignKey("myhome.MyHome",blank=True, on_delete=models.CASCADE)
    channels = models.ManyToManyField("myhome.Channel",blank=True)
    active = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name