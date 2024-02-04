from rest_framework import serializers
from vidcompressbot.models import VidSettingModel
from accounts.models import User
from vidcompressbot.models import SubVidModel , VidPlanModel



class VidPlanSerializer(serializers.ModelSerializer):
    class Meta :
        model = VidPlanModel
        fields = '__all__'


class VidSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VidSettingModel
        fields = '__all__'



class SubVidModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubVidModel
        fields = '__all__'




class UserSerializer(serializers.ModelSerializer):
    sub = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'

    def get_sub(self, obj):
        user_subs = obj.user_vid.sub.filter(is_active = True).first()
        serializer = SubVidModelSerializer(user_subs)
        return serializer.data
