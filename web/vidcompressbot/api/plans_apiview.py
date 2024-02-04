from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status , permissions
from vidcompressbot.models import VidPlanModel
from vidcompressbot.serializers import VidPlanSerializer



class GetPlansAPIView(APIView):
    authentication_classes = [TokenAuthentication ,]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    

    def get(self , request ):
        plans = VidPlanModel.objects.filter(is_active = True)
        ser_data = VidPlanSerializer(plans , many = True)
        return Response(ser_data.data)
