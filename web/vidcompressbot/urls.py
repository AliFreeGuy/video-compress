from django.urls import path
from vidcompressbot.api import VidSettingAPIView ,UserUpdateAPIView , GetPlansAPIView , VolumeChangeAPIView


app_name = 'vidcompressbot'


urlpatterns = [
    path('api/setting/', VidSettingAPIView.as_view() , name='setting'),
    path('api/user_update/' , UserUpdateAPIView.as_view() , name='user_update'),
    path('api/plans/' , GetPlansAPIView.as_view() ,name='plans') ,
    path('api/volume_change/' ,  VolumeChangeAPIView.as_view() , name='volume_change')
    
]