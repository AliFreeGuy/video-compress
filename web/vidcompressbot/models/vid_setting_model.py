from django.db import models
from core.models import BotModel
from django.core.validators import MinValueValidator, MaxValueValidator



class VidSettingModel(models.Model):
    bot = models.ForeignKey(BotModel , on_delete = models.CASCADE , verbose_name = 'telegram bot')
    video_limit = models.BigIntegerField(default = 500)
    is_active = models.BooleanField(default = True , verbose_name = 'bot status')
    not_active_text = models.TextField(default = 'خالی'  , verbose_name = 'bot text off')
    admin_chat_id = models.BigIntegerField(verbose_name = 'chat_id admin')
    support_id = models.CharField(max_length = 128 ,default = 'خالی' )
    support_text= models.TextField(default = 'خالی')
    help_text = models.TextField(default = 'خالی' )
    video_compressor_status = models.BooleanField(default = True)
    video_compressor_text = models.TextField(default = 'خالی')
    start_text = models.TextField(default = 'خالی' )
    restrict_saving_content = models.BooleanField(default = False)
    actication_sub_tex =models.TextField()
    user_not_active_text = models.TextField(default = 'خالی')
    watermark_text = models.CharField(max_length = 32 ,null = True , blank = True)
    channel_url  = models.CharField(max_length = 128 , null = True , blank = True)
    channel_chat_id  = models.BigIntegerField( null = True , blank = True)
    join_channel_text = models.TextField(default = 'خالی')
    quality_1 = models.IntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(500)
        ]
     , default = 100)
    quality_2 = models.IntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(500)
        ]
    , default = 100)
    quality_3 = models.IntegerField(
        validators=[
            MinValueValidator(100),
            MaxValueValidator(500)
        ]
    , default = 100)


    def __str__(self) -> str:
        return 'VidCompressBot Setting'
    


    
    class Meta :

        verbose_name = "Vid Setting"
        verbose_name_plural = "Vid Setting"