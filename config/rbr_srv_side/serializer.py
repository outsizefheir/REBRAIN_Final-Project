from rest_framework import serializers
from .models import Server, SystemInfo


class ServerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Server
        fields = ['id', 'ip_address', 'description', 'name']
        
class SystemInfoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SystemInfo
        fields = ['host_information', 'network', 'disk', 'memory', 'cpu', 'load_average']