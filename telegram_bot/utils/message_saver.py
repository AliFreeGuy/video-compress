import redis



r = redis.Redis(host='localhost' , db=0 , port=6379 , decode_responses=True)

def save_message(chat_id , message_id ):
        r.set(f'user_message:{str(chat_id)}:{str(message_id)}' , 'fuck')
        return True
    

def get_messages(chat_id):
        messages = r.keys(f'user_message:{str(chat_id)}:*')
        data = []
        for i in messages :
            message_id = i.split(':')[2]
            data.append(int(message_id))
        return data
    


