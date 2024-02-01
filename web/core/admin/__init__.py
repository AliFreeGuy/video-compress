from django.contrib import admin
from core.models.bot_model import BotModel
from core.models.bot_setting_model import BotSettingModel

admin.site.register(BotModel)
admin.site.register(BotSettingModel)