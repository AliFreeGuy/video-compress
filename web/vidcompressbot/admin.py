from django.contrib import admin
from vidcompressbot.models.user_vidcompressbot_model import UserVid
from vidcompressbot.models import VidPlanModel , SubVidModel , VidSettingModel

admin.site.register(UserVid)
from .models import SendMessageModel

class SendMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id',) 
    filter_horizontal = ('user',)

admin.site.register(SendMessageModel, SendMessageModelAdmin)



admin.site.register(VidPlanModel)
admin.site.register(SubVidModel)
admin.site.register(VidSettingModel)