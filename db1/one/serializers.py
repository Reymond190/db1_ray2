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

class mySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ray
        fields = [
'vin',
'date',
'time',
'status',
'startlocation',
'startodometer',
'running',
'idle',
'stop',
'inactive',
'endodometer',
'endlocation',
'distance',
'average',
'current_speed',
'maxstop',
'maxspeed',
'overspeed',
'alert',
'noidle',
'deviceImeiNo',
'plateNumber',
'No_of_iteration',
'latitude',
'longitude',
'direction',
'engine_current',
'Driver_Name',
'Device_Id',
'Vehicle_Type',
'Sim_Number',
'Device_Model',
'Vehicle_Licence_No',
'Device_Timezone']

class Serialize2(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = api1
        fields = ['id','Total','Running','Idle','Stop','Inactive','No_of_overspeed','No_of_geofence']

