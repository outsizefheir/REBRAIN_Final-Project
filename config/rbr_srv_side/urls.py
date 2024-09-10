from django.urls import path
from .views import ServerViewSet, ServerDetailView, ServerAddView, SystemInfoAddView, SystemInfoListView


urlpatterns = [
    path('servers/', ServerViewSet.as_view()),
    path('servers/<int:pk>', ServerDetailView.as_view()),
    path('servers/add', ServerAddView.as_view()),
    path('servers/add_data',SystemInfoAddView.as_view()),
    path('system_info/', SystemInfoListView.as_view()),  
]