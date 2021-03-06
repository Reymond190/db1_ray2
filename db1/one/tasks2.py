import requests
import json
from celery import shared_task
from pandas.io.json import json_normalize
import datetime
from celery.schedules import crontab
import string
from googlegeocoder import GoogleGeocoder
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
import json
from .models import ray
import requests

import time
from datetime import timedelta
import datetime
import pandas as pd
from pandas.io.json import json_normalize
import math

from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from .models import Alert ,api1


import pytz


def get_api():
    r1 = requests.get('http://13.235.62.229:8000/location/')
    x1 = r1.json()
    x2 = json.dumps(x1)
    y1 = json.loads(x2)
    df1 = json_normalize(y1)
    return df1


@shared_task
def exec():
    a = get_api()
    print(a)
    print(a.shape[0])
    df = a
    a1 = api1.objects.get(No="1")
    df2 = df.loc[(df["status"] == "running")]  # RUNNING VEHICLES
    df3 = df.loc[(df["status"] == "idle")]  # IDLE VEHICLES
    df4 = df.loc[(df["status"] == "stop")]  # STOP_VEHICLES
    df5 = df.loc[(df["status"] == 'inactive')]  # Inactive
    a1.id = "1"
    a1.Total = str(df.shape[0])
    a1.Running = str(df2.shape[0])
    a1.Idle = str(df3.shape[0])
    a1.Stop = str(df4.shape[0])
    a1.Inactive = str(df5.shape[0])
    a1.NoData = "temperarily unavailable"
    a1.No_of_geofence = "temperarily unavailable"
    a1.No_of_overspeed = "temperarily unavailable"
    a1.save()  # hello



    for i in range(df.shape[0]):
        v2 = ray()
        print('status'+str([i]),df['status'][i])
        if (ray.objects.filter(vin=df['device_imei'][i])):
            v3 = ray.objects.get(vin=df['device_imei'][i])
            if (str(df['engine_status'][i]) == 'ON' and df['speed'][i] > 0):  # running time calculation
                time1 = v3.running
                time1 = datetime.datetime.strptime(time1, '%H:%M:%S')
                x = time1 + timedelta(seconds=10)
                x = x.time()
                v3.running = str(x)  # changes existing running to updated time
                v3.endlocation = str(df['latitude'][i]) + "," + str(df['longitude'][i])
                v3.engine_current = "ON"


                if (df['speed'][i] > v3.maxspeed):  # check maxspeed with currentspeed
                    v3.maxspeed = df['speed'][i]
                if (str(df['status'][i]) == 'overspeed'):
                    v3.overspeed = v3.overspeed + 1
                    v3.alert = v3.alert + 1

            elif (str(df["engine_status"][i]) == "ON" and df['speed'][i] == 0):             #incase of idle time calculation
                time1 = datetime.datetime.strptime(v3.idle, '%H:%M:%S')
                x = time1 + timedelta(seconds=10)  # changes existing running to updated time
                x = x.time()
                v3.idle = str(x)
                v3.engine_current = "ON"
                v3.noidle = int(v3.noidle + 1)

            elif (str(df["engine_status"][i]) == "OFF" and df['speed'][i] == 0):  # stop
                v3.maxstop = v3.maxstop + 1
                time1 = datetime.datetime.strptime(v3.stop, '%H:%M:%S')
                x = time1 + timedelta(seconds=10)
                x = x.time()
                v3.stop = str(x)
                v3.engine_current = "OFF"

            else:
                print("Error")

            v3.average = round(v3.average + df['speed'][i] / 2)
            v3.endodometer = float(v3.endodometer + float(df['odometer'][i]))
            v3.No_of_iterations = v3.No_of_iterations + 1
            v3.distance = float(v3.distance + float(df['odometer'][i]))
            v3.direction = str(df['direction'][i])
            v3.latitude = str(df['latitude'][i])
            v3.longitude = str(df['longitude'][i])
            v3.save()
            
        
        else:
            time2 = datetime.datetime.now()
            tz = pytz.timezone('Asia/Kolkata')
            time2 = time2.astimezone(tz)
            v2.date = time2.date()
            ui = time2.time()
            v2.time = datetime.datetime.strptime(ui, '%H:%M:%S')
            v2.vin = df['deviceImeiNo'][i]
            v2.deviceImeiNo = df['deviceImeiNo'][i]
            v2.plateNumber = df['plateNumber'][i]
            v2.No_of_iterations = 0
            v2.startlocation = str(df['latitude'][i]) + ", " + str(df['longitude'][i])
            v2.endlocation = str(df['latitude'][i]) + ", " + str(df['longitude'][i])
            v2.startodometer = float(df['odometer'][i])
            v2.endodometer = float(df['odometer'][i])
            v2.distance = float(df['odometer'][i])
            if (str(df['status'][i]) == 'running' or str(df['status'][i]) == 'overspeed'):
                v2.running = "00:00:10"
                v2.stop = "00:00:00"
                v2.engine_current = "ON"
                v2.idle = "00:00:00"
            elif (str(df['status'][i]) == 'stop'):
                v2.stop = "00:00:10"
                v2.running = "00:00:00"
                v2.engine_current = "OFF"
                v2.idle = "00:00:00"
            else:
                v2.running = "00:00:00"
                v2.engine_current = "ON"
                v2.stop = "00:00:00"
                v2.idle = "00:00:10"

            v2.current_speed = df['speed'][i]
            v2.inactive = 0
            v2.noidle = 0
            v2.maxstop = 0
            v2.maxspeed = df['speed'][i]
            v2.average = df['speed'][i]
            v2.overspeed = 0
            v2.alert = 0
            v2.direction = str(df['direction'][i])
            v2.latitude = str(df['latitude'][i])
            v2.longitude = str(df['longitude'][i])
            v2.No_of_iterations = 0
            v2.save()
            print("saved")


