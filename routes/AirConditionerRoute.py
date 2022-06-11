from socket import socket
from controller import AirController # import users controller
ac = AirController.ac_controller()  # definisi dari user controller

def AllDevice():
    return ac.all_device() # get all

def RunningDevice(device_id,socket):
    return ac.running_device(device_id,socket) # start 

def StopDevice(device_id,socket):
    return ac.stop_device(device_id,socket) # stop

def CallbackEventDevice(device_id,status,message,socket):
    return ac.callback_events(device_id=device_id,status=status,message=message,socket=socket) # recieve