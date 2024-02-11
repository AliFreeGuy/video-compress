
from celery import shared_task
from vidcompressbot.models.send_message_model import SendMessageModel
import time
from vidcompressbot.utils import send_message
from core.models.bot_model import BotModel

@shared_task
def send_message_task(msg_id):
    try :
        msg = SendMessageModel.objects.filter(id = msg_id)
        if msg.exists():

            bot = BotModel.objects.filter(username = 'vidcompressbot').first()
            msg = msg.first()
            users = msg.user.all()
            
            for user in users :
                res = send_message(chat_id=int(user.user.chat_id) , message=msg.message , bot_token=bot.token)
                time.sleep(0.2)
            return True
        

    except Exception as e :
        return e
    



@shared_task
def send_quick_message(chat_id , message ):
    try :

        bot = BotModel.objects.filter(username = 'vidcompressbot').first()
        res  = send_message(chat_id=int(chat_id)  , message=message ,bot_token=bot.token)
        print(res)

    except Exception as e :
        return e 