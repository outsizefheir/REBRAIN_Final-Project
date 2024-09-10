from django.db import models

class Server(models.Model):

    name = models.CharField('name', max_length=255)
    ip_address = models.GenericIPAddressField('IP', max_length=16, default='0.0.0.0')
    description = models.TextField('description', max_length=255, default='no_description')

    class Meta:
        managed = True
        verbose_name = 'Server'
        
class SystemInfo(models.Model):
    
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    host_information = models.JSONField('host_information')
    network = models.JSONField('network')
    disk = models.JSONField('disk')
    memory = models.JSONField('memory')
    cpu = models.JSONField('cpu')
    load_average = models.JSONField('load_average')

    class Meta:
        managed = True
        verbose_name = 'System Information'