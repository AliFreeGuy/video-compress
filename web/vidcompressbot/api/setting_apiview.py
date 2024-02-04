from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  ,permissions
from vidcompressbot.models import VidSettingModel
from vidcompressbot.serializers import VidSettingSerializer
from vidcompressbot.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication




class VidSettingAPIView(APIView):
    authentication_classes = [TokenAuthentication ,]
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        vid_settings = VidSettingModel.objects.first()
        serializer = VidSettingSerializer(vid_settings)
        return Response(serializer.data , status=status.HTTP_200_OK)
    



