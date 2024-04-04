
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from accounts.models import User
from vidcompressbot.models import UserVid , VidPlanModel , SubVidModel
from core.models import BotModel







@receiver(post_save, sender=UserVid)
def add_free_sub_for_new_user(sender, instance, created, **kwargs):
    if created:
        free_sub = VidPlanModel.objects.filter(tag = 'free').first()

        if free_sub :
            try :

                user = instance 
                bot = BotModel.objects.filter(username = 'vidcompressbot').first()
                data = SubVidModel.objects.create(bot = bot , user = user , plan = free_sub)
            except Exception as e :
                print(f'ERROR: {str(e)}')