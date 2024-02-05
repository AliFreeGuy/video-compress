from django.contrib import admin
from core.models.bot_model import BotModel
from core.models.bot_setting_model import BotSettingModel


from django.contrib import admin
from core.models import BotModel

class BotModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'username', 'token')
    search_fields = ('name', 'username', 'token')
    ordering = ('name',)

admin.site.register(BotModel, BotModelAdmin)







from django.contrib import admin
from core.models import BotSettingModel

class BotSettingModelAdmin(admin.ModelAdmin):
    list_display = ('bot', 'key', 'val', 'setting')
    search_fields = ('bot__name', 'key', 'val')
    list_filter = ('bot',)
    ordering = ('bot', 'key')

admin.site.register(BotSettingModel, BotSettingModelAdmin)
