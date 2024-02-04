from django.urls import path
from vidcompressbot.api import VidSettingAPIView ,UserUpdateAPIView


app_name = 'vidcompressbot'


urlpatterns = [
    path('api/setting/', VidSettingAPIView.as_view() , name='setting'),
    path('api/user_update/' , UserUpdateAPIView.as_view() , name='user_update')
    
]