from django.contrib import admin
from .models import Server, SystemInfo

@admin.register(Server)
class ServerAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'name', 'description')
    
@admin.register(SystemInfo)
class SystemInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'server', 'host_information', 'network', 'disk', 'memory', 'cpu', 'load_average')
    search_fields = ('server__name',)
    list_filter = ('server',)