
from rest_framework import viewsets, generics, status
from django.shortcuts import render

# from googlegeocoder import GoogleGeocoder
from requests.auth import HTTPBasicAuth
# from django.http import HttpResponse
import json
import requests
from django.db.models import Q
from datetime import timedelta
import datetime
from pandas.io.json import json_normalize
from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response

from .models import ray, api1

from .serializers import GroupSerializer, Serialize2,mySerializer, ticket_serializer




from celery.schedules import crontab

import json
from .models import ray
import requests

import time
from datetime import timedelta
import datetime
import pandas as pd
from pandas.io.json import json_normalize
import math

from .models import Alert, api1, Tickets

import pytz


def home(request):
    return render(request,'home.html')


def get_api():
    r1 = requests.get('http://13.235.62.229/location/')
    x1 = r1.json()
    x2 = json.dumps(x1)
    y1 = json.loads(x2)
    df1 = json_normalize(y1)
    return df1



def all2(request):
    a = get_api()
    print(a.shape[0])
    df = a
    if (api1.objects.filter(id=1)):
        a1 = api1.objects.get(id=1)
    else:
        a1 = api1()

    try:
        df1 = ray.objects.all().count()
        df2 = ray.objects.filter(status = 'running').count()  # RUNNING VEHICLES
        df3 = ray.objects.filter(status = 'idle').count()  # IDLE VEHICLES
        df4 = ray.objects.filter(status = 'stop').count()  # STOP_VEHICLES
        df5 = ray.objects.filter(status = 'Inactive').count()  # Inactive
        a1.Total = str(df1 if df1==0 else df1+1)
        a1.Running = str(df2 if df2==0 else df2+1)
        a1.Idle = str(df3 if df3==0 else df3+1)
        a1.Stop = str(df4 if df4==0 else df4+1)
        a1.Inactive = str(df5 if df5==0 else df5+1)
        a1.No_of_geofence = "temperarily unavailable"
        a1.No_of_overspeed = "temperarily unavailable"
        a1.save()  # hello

    except:

        if (api1.objects.filter(id=1)):
            a1 = api1.objects.get(id=1)
        else:
            a1 = api1()
        a1.Total = "temperarily unavailable"
        a1.Running = "temperarily unavailable"
        a1.Idle = "temperarily unavailable"
        a1.Stop = "temperarily unavailable"
        a1.Inactive = "temperarily unavailable"
        a1.No_of_geofence = "temperarily unavailable"
        a1.No_of_overspeed = "temperarily unavailable"
        a1.save()  # hello


    for i in range(df.shape[0]):
        time2 = datetime.datetime.now()
        tz = pytz.timezone('Asia/Kolkata')
        time2 = time2.astimezone(tz)
        time2 = time2.strftime("%d-%m-%Y %H:%M:%S")
        time4 = datetime.datetime.strptime(time2, '%d-%m-%Y %H:%M:%S')

        if (ray.objects.filter(deviceImeiNo=df['device_imei'][i])):
            v3 = ray.objects.get(deviceImeiNo=df['device_imei'][i])
            v3.average = round(v3.average + int(df['speed'][i]) / 2)
            v3.endodometer = float(v3.endodometer + float(df['odometer'][i]))
            v3.No_of_iterations = v3.No_of_iterations + 1
            v3.distance = float(v3.distance + float(df['odometer'][i]))
            v3.direction = str(df['direction'][i])
            v3.latitude = str(df['latitude'][i])
            v3.longitude = str(df['longitude'][i])
            # inactive calc

            servertime = datetime.datetime.strptime(df['serv_date'][i], '%d-%m-%Y %H:%M:%S')

            resulttime = time4 - servertime

            statictime = timedelta(minutes=5)

            if (resulttime < statictime):
                if (str(df['engine_status'][i]) == 'ON' and int(df['speed'][i]) > 0):  # running time calculation
                    time1 = v3.running
                    time1 = datetime.datetime.strptime(time1, '%H:%M:%S')
                    x = time1 + timedelta(seconds=10)
                    x = x.time()
                    v3.running = str(x)  # changes existing running to updated time
                    v3.endlocation = str(df['latitude'][i]) + "," + str(df['longitude'][i])
                    v3.engine_current = "ON"
                    v3.current_speed = int(df['speed'][i])
                    v3.status = 'running'

                    if (int(df['speed'][i]) > v3.maxspeed):  # check maxspeed with currentspeed
                        v3.maxspeed = int(df['speed'][i])
                    if (str(df['status'][i]) == 'overspeed'):
                        v3.overspeed = v3.overspeed + 1
                        v3.alert = v3.alert + 1
                        v3.status = 'overspeed'

                elif (str(df["engine_status"][i]) == "ON" and int(
                        df['speed'][i]) == 0):  # incase of idle time calculation
                    time1 = datetime.datetime.strptime(v3.idle, '%H:%M:%S')
                    x = time1 + timedelta(seconds=10)  # changes existing running to updated time
                    x = x.time()
                    v3.idle = str(x)
                    v3.engine_current = "ON"
                    v3.current_speed = 0
                    v3.noidle = int(v3.noidle + 1)
                    v3.status = 'idle'

                elif (str(df["engine_status"][i]) == "OFF" and int(df['speed'][i]) == 0):  # stop
                    v3.maxstop = v3.maxstop + 1
                    time1 = datetime.datetime.strptime(v3.stop, '%H:%M:%S')
                    x = time1 + timedelta(seconds=10)
                    x = x.time()
                    v3.stop = str(x)
                    v3.current_speed = 0
                    v3.engine_current = "OFF"
                    v3.status = 'stop'

                else:
                    print("Error")
            else:
                time1 = datetime.datetime.strptime(v3.inactive, '%H:%M:%S')
                x = time1 + timedelta(seconds=10)  # changes existing running to updated time
                x = x.time()
                v3.inactive = str(x)
                v3.engine_current = "Inactive"
                v3.status = 'Inactive'

            print('saved')

            v3.save()


        else:
            v2 = ray()
            time2 = datetime.datetime.now()
            tz = pytz.timezone('Asia/Kolkata')
            time2 = time2.astimezone(tz)
            v2.date = time2.date()
            ui = time2.time()
            v2.time = ui.strftime("%H:%M:%S")
            v2.vin = df['Device_Id'][i]

            v2.deviceImeiNo = df['device_imei'][i]
            v2.plateNumber = df['Vehicle_Number'][i]
            v2.Driver_Name = df['Driver_Name'][i]
            v2.Vehicle_Number = df['Driver_Name'][i]
            v2.Vehicle_Type = df['Driver_Name'][i]
            v2.Sim_Number = df['Driver_Name'][i]
            v2.IMEI_Number = df['Driver_Name'][i]
            v2.Device_Model = df['Driver_Name'][i]
            v2.Vehicle_Licence = df['Driver_Name'][i]
            v2.Device_Timezone = df['Driver_Name'][i]
            v2.No_of_iterations = 0
            v2.startlocation = str(df['latitude'][i]) + ", " + str(df['longitude'][i])
            v2.endlocation = str(df['latitude'][i]) + ", " + str(df['longitude'][i])
            v2.startodometer = float(df['odometer'][i])
            v2.endodometer = float(df['odometer'][i])
            v2.distance = float(df['odometer'][i])

            servertime = datetime.datetime.strptime(df['serv_date'][i], '%d-%m-%Y %H:%M:%S')

            resulttime = time4 - servertime

            statictime = timedelta(minutes=5)

            if (resulttime < statictime):
                v2.inactive = "00:00:00"
                if (str(df['status'][i]) == 'running' or str(df['status'][i]) == 'overspeed'):
                    v2.running = "00:00:10"
                    v2.current_speed = int(df['speed'][i])
                    v2.engine_current = "ON"
                    v2.status = 'running'

                elif (str(df['status'][i]) == 'stop'):
                    v2.stop = "00:00:10"
                    v2.current_speed = 0
                    v2.engine_current = "OFF"
                    v2.status = 'stop'

                else:
                    v2.engine_current = "ON"
                    v2.current_speed = 0
                    v2.idle = "00:00:10"
                    v2.status = 'idle'

            else:
                v2.current_speed = 0
                v2.inactive = "00:00:10"
                v2.status = 'Inactive'
                v2.engine_current = 'Inactive'

            v2.noidle = 0
            v2.maxstop = 0
            v2.maxspeed = int(df['speed'][i])
            v2.average = int(df['speed'][i])
            v2.overspeed = 0
            v2.alert = 0
            v2.stop = "00:00:00"
            v2.running = "00:00:00"
            v2.idle = "00:00:00"
            v2.direction = str(df['direction'][i])
            v2.latitude = str(df['latitude'][i])
            v2.longitude = str(df['longitude'][i])
            v2.No_of_iterations = 0
            v2.save()
            print("saved")

    return render(request,'home.html')




# class ApiList(APIView):
#
#     def get(self, request):
#         g = ray.objects.all()
#         serializer=GroupSerializer(g)
#         return Response(serializer.data)


class ApiViewSet(viewsets.ModelViewSet):
    queryset = ray.objects.all()
    serializer_class = GroupSerializer

class SingleApi(viewsets.ModelViewSet):
    queryset = api1.objects.all()
    serializer_class = Serialize2

def get_dataframe(y1):
    df1 = json_normalize(y1["assetHistory"])
    return df1





class FilterList(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """

        q = self.kwargs['vin']

        p = ray.objects.filter(Q(vin__icontains=q)|Q(plateNumber__icontains=q)|Q(status__icontains=q)|Q(engine_current__icontains=q)|Q(deviceImeiNo__icontains=q))

        return p

class FilterList2(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        p = ray.objects.all()
        return p

class Myfilter(generics.ListAPIView):
    serializer_class = mySerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        q = self.kwargs['vin']

        p = ray.objects.filter(Q(vin__icontains=q) | Q(plateNumber__icontains=q) | Q(status__icontains=q) | Q(
            engine_current__icontains=q) | Q(deviceImeiNo__icontains=q))

        return p

class Myfilter2(generics.ListAPIView):
    serializer_class = mySerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        p = ray.objects.all()
        return p



class ClassicList(generics.ListAPIView):
    serializer_class = Serialize2

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        p = api1.objects.all()
        return p


class Ticketupdate(generics.ListAPIView):
    serializer_class = ticket_serializer

    def get_queryset(self,pk):
        try:
            ticket = Tickets.objects.get(pk=self.kwargs['pk'])
        except Tickets.DoesNotExist:
            print('error')
            return Response(status=status.HTTP_404_NOT_FOUND)
        return ticket

    def get(self, request,pk):

        movie = self.get_queryset(self.kwargs['pk'])
        serializer = ticket_serializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)




    def put(self, request, pk):
        Tickets = self.get_queryset(self.kwargs['pk'])
        serializer = ticket_serializer(Tickets, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        ticket = self.get_queryset(self.kwargs['pk'])
        ticket.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TicketView(ListCreateAPIView):
    serializer_class = ticket_serializer

    def get_queryset(self):
        ticket = Tickets.objects.all()
        return ticket


    def post(self, request):
        serializer = ticket_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

