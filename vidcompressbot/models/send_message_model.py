from django.db import models
from vidcompressbot.models import UserVid



class SendMessageModel(models.Model):
    user = models.ManyToManyField(UserVid, related_name='admin_message')
    message = models.TextField()
    creation = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return str(self.message[:30])

    
    class Meta :

        verbose_name = "Vid SendMessage"
        verbose_name_plural = "Vid SendMessage"