from django.contrib import admin
from vidcompressbot.models.user_vidcompressbot_model import UserVid
from vidcompressbot.models import VidPlanModel , SubVidModel , VidSettingModel
from vidcompressbot.models import SendMessageModel
from django.contrib import admin
from django.utils import timezone
from jdatetime import datetime
from .models import SubVidModel
from django.contrib import admin
from .models import UserVid
from django.contrib import admin
from jdatetime import datetime
from .models import UserVid
from django.contrib import admin
from .models import VidSettingModel


class VidSettingModelAdmin(admin.ModelAdmin):
    list_display = ( 'bot','is_active', 'admin_chat_id')
    search_fields = ('bot__name', 'admin_chat_id')
    list_filter = ('is_active',)
    ordering = ('-id',)
admin.site.register(VidSettingModel, VidSettingModelAdmin)


class UserVidAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_creation_jalali')
    search_fields = ('user__full_name__icontains', 'user__chat_id__icontains')
    ordering = ('-creation',)
    def get_creation_jalali(self, obj):
        return datetime.fromgregorian(datetime=obj.creation).strftime('%Y/%m/%d %H:%M:%S')
    get_creation_jalali.short_description = 'Creation (Jalali)'
admin.site.register(UserVid, UserVidAdmin)


class VidPlanModelAdmin(admin.ModelAdmin):
    list_display = ( 'tag', 'name', 'day', 'volum', 'price', 'is_active')
    search_fields = ('bot__name', 'tag', 'name', 'day', 'volum', 'price')
    list_filter = ('bot', 'is_active')
    ordering = ('bot', 'name')
admin.site.register(VidPlanModel , VidPlanModelAdmin)



class SendMessageModelAdmin(admin.ModelAdmin):
    list_display = ('message', 'creation')
    filter_horizontal = ('user',)
    search_fields = ('message',)
    ordering = ('-creation',)
admin.site.register(SendMessageModel, SendMessageModelAdmin)



class SubVidModelAdmin(admin.ModelAdmin):
    list_display = ( 'user', 'plan', 'get_expiry_jalali_with_remaining_days', 'volum', 'volum_used', 'is_active')
    list_filter = ('bot', 'is_active')
    search_fields = ('user__user__full_name__icontains', 'user__user__chat_id__icontains')
    ordering = ('-id',)
    def get_expiry_jalali_with_remaining_days(self, obj):
        expiry_jalali = datetime.fromgregorian(datetime=obj.expiry).strftime('%Y/%m/%d')
        remaining_days = (obj.expiry - timezone.now()).days
        return f'{expiry_jalali} - {remaining_days} days'
    get_expiry_jalali_with_remaining_days.short_description = 'Expiry with Remaining Days'
admin.site.register(SubVidModel, SubVidModelAdmin)