
from django.db.models.signals import post_save , pre_save
from django.dispatch import receiver
from vidcompressbot.models import SendMessageModel
from vidcompressbot.tasks import send_message_task
from vidcompressbot.models import SubVidModel
from vidcompressbot.tasks import send_quick_message



@receiver(post_save, sender=SubVidModel)
def activation_user_sub_notification(sender, instance, created, **kwargs):
    if created:
        send_quick_message.delay(chat_id=instance.user.user.chat_id , message='اشتراک شما با موفقیت فعال شد')
        