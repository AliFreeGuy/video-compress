from rest_framework.views import APIView
from rest_framework.response import Response 
from vidcompressbot.models import UserVid
from accounts.models import User
from vidcompressbot.serializers import UserSerializer
from vidcompressbot.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status  ,permissions
from rest_framework.serializers import ValidationError




class UserUpdateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def post(self, request):
        try:
            user = User.objects.filter(chat_id=request.data.get('chat_id'))

            if not user.exists():
                data = request.data
                new_user, created = User.objects.get_or_create(chat_id=data.get('chat_id'), full_name=data.get('full_name'))
                UserVid(user=new_user).save()
                return Response(UserSerializer(new_user).data, status=status.HTTP_200_OK)
            
            user = user.first()
            
            if request.data.get('full_name'):
                user.full_name = request.data.get('full_name')
                user.save()

            print('##########################################')
            print(user.user_vid.sub_updater())

            print('##########################################')

            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)