from rest_framework import serializers
from vidcompressbot.models import VidSettingModel

class VidSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = VidSettingModel
        fields = '__all__'
