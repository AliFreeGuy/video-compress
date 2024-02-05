from django.db import models
from core.models import BotModel



class VidPlanModel(models.Model):
    bot = models.ForeignKey(BotModel , on_delete = models.CASCADE , related_name = 'plans')
    tag = models.CharField(max_length = 128  , unique = True)
    name = models.CharField(max_length = 128, unique = True) 
    day  = models.IntegerField()
    volum = models.IntegerField()
    des = models.TextField()
    price = models.IntegerField()
    is_active = models.BooleanField(default = True)


    def __str__(self) -> str:
        return str(self.name)
    

    class Meta :

        verbose_name = "Vid Plans"
        verbose_name_plural = "Vid Plans"