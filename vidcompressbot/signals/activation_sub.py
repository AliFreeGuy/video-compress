
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from vidcompressbot.models import SendMessageModel
from vidcompressbot.tasks import send_message_task
from vidcompressbot.models import SubVidModel
from vidcompressbot.tasks import send_quick_message
from vidcompressbot.models import VidSettingModel


@receiver(post_save, sender=SubVidModel)
def activation_user_sub_notification(sender, instance, created, **kwargs):
    if created:
        setting = VidSettingModel.objects.first()
        if setting :send_quick_message.delay(chat_id=instance.user.user.chat_id , message=setting.actication_sub_tex)
        else :send_quick_message.delay(chat_id=instance.user.user.chat_id , message='اشتراک شما فعال شد')
        