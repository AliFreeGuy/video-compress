import requests
from django.conf import settings

def send_message(chat_id , message, bot_token ):
        try :
            if settings.DEBUG == False:
                url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
                payload = {'chat_id': chat_id,'text': message}
                return  requests.post(url, data=payload )
            return f'debug is on : sended message : {message}'  
        except Exception as e :
            return e



def edit_message(chat_id, message_id, text, bot_token):
    url = f'https://api.telegram.org/bot{bot_token}/editMessageText'
    payload = {'chat_id': chat_id, 'message_id': message_id, 'text': text}
    response = requests.post(url, data=payload)


