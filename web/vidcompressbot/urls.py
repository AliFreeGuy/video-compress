from django.urls import path
from vidcompressbot.api import VidSettingAPIView


app_name = 'vidcompressbot'


urlpatterns = [
    path('api/setting/', VidSettingAPIView.as_view() , name='setting'),
    
]