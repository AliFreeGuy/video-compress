from django.db import models
from accounts.models.user_model import User
from core.models.bot_model import BotModel
from django.utils import timezone

class UserVid(models.Model):
    user = models.OneToOneField(User , on_delete = models.CASCADE , related_name = 'user_vid')
    creation = models.DateTimeField(auto_now_add = True)


    def __str__(self) -> str:
        return str(self.user)
    
    def sub_updater(self):
        subscriptions = self.sub.filter(is_active=True)
        for sub in subscriptions:
            if sub.expiry < timezone.now():
                sub.is_active = False
                sub.save()
        
    
    class Meta :

        verbose_name = "Vid Users"
        verbose_name_plural = "Vid Users"