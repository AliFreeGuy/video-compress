from core.models.bot_model import BotModel
from django.db import models


class BotSettingModel(models.Model):
    bot = models.ForeignKey(BotModel , on_delete = models.CASCADE , related_name = 'setting')
    key = models.CharField(max_length = 200 )
    val =  models.CharField(max_length = 200 , null = True , blank = True)
    setting = models.JSONField(null = True , blank = True)

    def __str__(self) -> str:
        return f'{self.bot} - {self.key}'
    


    class Meta :

        verbose_name = "General Setting"
        verbose_name_plural = "General Setting"