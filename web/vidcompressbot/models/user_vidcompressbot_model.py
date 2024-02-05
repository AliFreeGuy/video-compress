from django.db import models
from accounts.models.user_model import User
from core.models.bot_model import BotModel


class UserVid(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , related_name = 'user_vid')
    creation = models.DateTimeField(auto_now_add = True)


    def __str__(self) -> str:
        return str(self.user)
    

    
    class Meta :

        verbose_name = "Vid Users"
        verbose_name_plural = "Vid Users"