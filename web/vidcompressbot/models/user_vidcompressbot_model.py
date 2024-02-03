from django.db import models
from accounts.models.user_model import User
from core.models.bot_model import BotModel


class UserVid(models.Model):
    bot = models.ForeignKey(BotModel , on_delete = models.CASCADE , related_name= 'users')
    user = models.ForeignKey(User , on_delete = models.CASCADE , related_name = 'user_vid')
    creation = models.DateTimeField(auto_now_add = True)


    def __str__(self) -> str:
        return self.user
    
