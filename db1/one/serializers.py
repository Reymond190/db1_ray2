from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ray , api1

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ray
        fields = ['vin' ,'date', 'time', 'startlocation', 'startodometer', 'running',\
    'idle', 'stop', 'inactive', 'endodometer', 'endlocation','status', 'distance',\
    'average','maxstop', 'maxspeed', 'overspeed', 'alert',\
    'deviceImeiNo', 'noidle', 'plateNumber', 'No_of_iterations', 'engine_current', 'current_speed','latitude',
    'longitude','direction']


class Serialize2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = api1
        fields = ['id','Total','Running','Idle','Stop','Inactive','No_of_overspeed','No_of_geofence']

