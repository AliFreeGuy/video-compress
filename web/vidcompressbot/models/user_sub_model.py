from django.db import models
from django.utils import timezone
import datetime
from core.models import BotModel
from vidcompressbot.models import UserVid ,VidPlanModel


class SubVidModel(models.Model):
    bot = models.ForeignKey(BotModel , on_delete=models.CASCADE )
    user = models.ForeignKey(UserVid , on_delete=models.CASCADE , related_name='sub' , null=True , blank=True)
    plan= models.ForeignKey(VidPlanModel , on_delete=models.CASCADE  , null=True , blank=True)
    expiry = models.DateTimeField(null=True , blank=True)
    volum = models.IntegerField(default=0 , null= True , blank=True)
    volum_used = models.IntegerField(default=0 , null=True , blank = True)
    is_active = models.BooleanField(default=True)



    @property
    def re_volum(self):
        return int(int(self.volum )- int(self.volum_used))
    

    def decrease(self, amount):
            self.volum_used+= amount
            self.save()

    def save(self, *args, **kwargs):
        active_subscription = SubVidModel.objects.filter(user=self.user, is_active=True).exclude(id=self.id).first()

        if active_subscription:
            active_subscription.is_active = False
            active_subscription.save()

        data = SubVidModel.objects.filter(id=self.id)

        if self.plan and not data.exists():
            self.expiry = datetime.datetime.now() + datetime.timedelta(days=int(self.plan.day))
            self.volum = self.plan.volum
            if self.user and self.user.sub.filter(is_active=True).exists():
                self.user.sub.filter(is_active=True).update(is_active=False)
                self.is_active = True

        super().save(*args, **kwargs)




    def __str__(self) -> str:
        return str(self.user)
    
    class Meta :

        verbose_name = "Vid User Subscription"
        verbose_name_plural = "Vid User Subscription"