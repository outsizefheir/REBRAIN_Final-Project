from rest_framework import generics
from .serializer import ServerSerializer, SystemInfoSerializer
from .models import Server, SystemInfo

class ServerViewSet(generics.ListAPIView):

    queryset = Server.objects.all()
    serializer_class = ServerSerializer

class ServerAddView(generics.CreateAPIView):
    queryset = Server.objects.all()
    serializer_class = ServerSerializer

    def perform_create(self, serializer):
        name = serializer.validated_data['name']
        instance, created = Server.objects.get_or_create(
            name=name,
            defaults={
                'description': serializer.validated_data['description'],
                'ip_address': serializer.validated_data['ip_address'],
            }
        )
        if not created:
            instance.description = serializer.validated_data['description']
            instance.ip_address = serializer.validated_data['ip_address']
            instance.save()

class ServerDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Server.objects.all()
    serializer_class = ServerSerializer
    
class SystemInfoAddView(generics.CreateAPIView):
    
    queryset = SystemInfo.objects.all()
    serializer_class = SystemInfoSerializer

    def perform_create(self, serializer):
        server_name = self.request.data.get('server')
        try:
            server_obj = Server.objects.get(name=server_name)
            serializer.save(server=server_obj)
        except Server.DoesNotExist:
            raise serializer.ValidationError("Server with this name does not exist.")
        
class SystemInfoListView(generics.ListAPIView):
    
    queryset = SystemInfo.objects.all()
    serializer_class = SystemInfoSerializer