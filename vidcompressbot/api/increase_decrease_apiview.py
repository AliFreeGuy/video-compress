from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework import status , permissions
from vidcompressbot import forms
from accounts.models import User



class VolumeChangeAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]
    def post(self, request):
        form = forms.VolumeChangeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = User.objects.filter(chat_id=data['user']).first()
            user_sub = user.user_vid.sub.filter(is_active=True).first()
            if user_sub:
                user_volume = user_sub.volum
                user_volume_used = user_sub.volum_used

                if data['operation_type'] == 'increase':
                    new_volume_used = user_volume_used + data['size']
                    if new_volume_used <= user_volume:
                        user_sub.volum_used = new_volume_used
                        user_sub.save()
                        response_data = {
                            'message': 'Success',
                            'volume': user_volume,
                            'volume_used': int(new_volume_used)
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Consumption volume is more than the total volume'}, status=status.HTTP_400_BAD_REQUEST)
                elif data['operation_type'] == 'decrease':
                    new_volume_used = user_volume_used - data['size']
                    if new_volume_used >= 0:
                        user_sub.volum_used = new_volume_used
                        user_sub.save()
                        response_data = {
                            'message': 'Success',
                            'volume': user_volume,
                            'volume_used': int(new_volume_used)
                        }
                        return Response(response_data, status=status.HTTP_200_OK)
                    else:
                        return Response({'error': 'Consumption volume is less than zero'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'error': 'Invalid form'}, status=status.HTTP_400_BAD_REQUEST)
