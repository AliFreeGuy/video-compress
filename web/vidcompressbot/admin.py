from django.contrib import admin
from vidcompressbot.models.user_vidcompressbot_model import UserVid


admin.site.register(UserVid)
from .models import SendMessageModel

class SendMessageModelAdmin(admin.ModelAdmin):
    list_display = ('id',) 
    filter_horizontal = ('user',)

admin.site.register(SendMessageModel, SendMessageModelAdmin)
