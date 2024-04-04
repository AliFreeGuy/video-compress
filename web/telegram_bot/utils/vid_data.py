from dotmap import DotMap
import redis
import json
import random




async def addvid(chat_id, name=None, thumbnail=None, quality=None, vid1=None,
                  vid2=None, vid3=None, task_id=None, status=None ,
                  vidvol1=None , vidvol2 =None, vidvol3= None,message_id = None  ):
        r = redis.Redis(host='localhost', port=6379, db=0 , decode_responses=True)
        key = f'uservid:{str(chat_id)}'
        if r.exists(key):r.delete(key)

        data = {
            'id' : random.randint(0  ,999999),
            "chat_id": chat_id,
            "name": str(name),
            "thumbnail": str(thumbnail),
            "quality": str(quality),
            "vid1": str(vid1),
            "vid2": str(vid2),
            "vid3": str(vid3),
            "vidvol1" : str(vidvol1),
            "vidvol2" : str(vidvol2),
            "vidvol3" : str(vidvol3),
            "task_id": str(task_id),
            "status": str(status),
            "message_id" : str(message_id)
        }
        r.hmset(key, data)
        dot_data = DotMap(data)

        return dot_data


async def getvid(chat_id):
        r = redis.Redis(host='localhost', port=6379, db=0 , decode_responses=True)
        key = f'uservid:{str(chat_id)}'
        data = r.hgetall(key)
        if data:return DotMap(data)
        else:None 
    



async def updatevid(chat_id, key, val):
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        userkey = f'uservid:{str(chat_id)}'
        if r.exists(userkey):
            r.hset(userkey, key, val)
            return DotMap(r.hgetall(userkey))
        else:
            return False 
    
    


async def save_message(chat_id , message_id ):
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        r.set(f'user_message:{str(chat_id)}:{str(message_id)}' , 'fuck')
        return True




async def get_messages(chat_id):
        r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
        messages = r.keys(f'user_message:{str(chat_id)}:*')
        data = []
        for i in messages :
            message_id = i.split(':')[2]
            data.append(int(message_id))
        return data
