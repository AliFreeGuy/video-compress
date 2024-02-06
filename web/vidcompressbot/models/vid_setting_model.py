from django.db import models
from core.models import BotModel




class VidSettingModel(models.Model):
    bot = models.ForeignKey(BotModel , on_delete = models.CASCADE , verbose_name = 'telegram bot')
    is_active = models.BooleanField(default = True , verbose_name = 'bot status')
    not_active_text = models.TextField(default = 'خالی'  , verbose_name = 'bot text off')
    admin_chat_id = models.IntegerField(verbose_name = 'chat_id admin')
    support_id = models.CharField(max_length = 128 ,default = 'خالی' )
    support_text= models.TextField(default = 'خالی')
    help_text = models.TextField(default = 'خالی' )
    video_compressor_status = models.BooleanField(default = True)
    video_compressor_text = models.TextField(default = 'خالی')
    start_text = models.TextField(default = 'خالی' )
    restrict_saving_content = models.BooleanField(default = False)
    actication_sub_tex =models.TextField(default = 'خالی')
    user_not_active_text = models.TextField(default = 'خالی')




    def __str__(self) -> str:
        return 'VidCompressBot Setting'
    


    
    class Meta :

        verbose_name = "Vid Setting"
        verbose_name_plural = "Vid Setting"