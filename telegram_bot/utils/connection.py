import redis
import time
import json
import requests
from utils.connection import connection as con 
from dotenv import load_dotenv
import os



api_hash = os.getenv("API_HASH")
api_id =  os.getenv("API_ID")
bot_token = os.getenv("BOT_TOKEN")
plugins = dict(root=os.getenv("PLUGINS_ROOT"))
proxy = {"scheme": os.getenv("PROXY_SCHEME"),
         "hostname": os.getenv("PROXY_HOSTNAME"),
         "port": int(os.getenv("PROXY_PORT"))}
api_key=os.getenv("API_KEY")
api_url = os.getenv("API_URL")
bot_username=os.getenv("BOT_USERNAME")
backup_channel =  os.getenv("BACKUP_CHANNEL")
    
class VidConnec:
    def __init__(self , api_key , url , bot_username) -> None:
        self.api_key = api_key
        self.url = url
        self.username = bot_username
        self.headers = {'Authorization' : f'token {self.api_key}'}
        self.redis_client = redis.Redis(host='localhost', port=6379, db=0) 

            


    @property
    def setting(self):
            last_request_time = self.redis_client.get('last_request_time')  
            current_time = time.time()
            if last_request_time is None or current_time - float(last_request_time) > 60:
                pattern = 'setting'
                url = self.link_generator(pattern=pattern)
                res = self.get(url)
                if res and res.status_code == 200:
                    res_data = res.json()
                    self.redis_client.set('setting_data', json.dumps(res_data))
                    self.redis_client.set('last_request_time', current_time)
                    return Response(res.json())
            else:
                return Response(json.loads(self.redis_client.get('setting_data')))
        

    
    @property
    def plans(self):
            last_request_time = self.redis_client.get('last_plans_request_time')  
            current_time = time.time()
            if last_request_time is None or current_time - float(last_request_time) > 60:
                pattern = 'plans'
                url = self.link_generator(pattern=pattern)
                res = self.get(url)
                if res and res.status_code == 200:
                    res_data = res.json()
                    self.redis_client.set('plans_data', json.dumps(res_data))
                    self.redis_client.set('last_plans_request_time', current_time)
                    return res_data
            else:
                return json.loads(self.redis_client.get('plans_data'))
        


    def user(self, chat_id , full_name):
            last_request_time = self.redis_client.get(f'last_user_request_time:{str(chat_id)}')  
            current_time = time.time()
            if last_request_time is None or current_time - float(last_request_time) > 60:

                pattern  = 'user_update'
                url = self.link_generator(pattern)
                res = self.post(url , chat_id  , full_name)
                res_raw = res
                if res and res.status_code == 200 :
                    res = Response(res.json())
                    self.redis_client.set(f'user_data:{str(chat_id)}', json.dumps(res_raw.json()))
                    self.redis_client.set(f'last_user_request_time:{str(chat_id)}', current_time)
                    return res
            else :
                return Response(json.loads(self.redis_client.get(f'user_data:{str(chat_id)}')))
            return None 
        
    
    def get_user(self , chat_id):
            pattern  = 'user_update'
            url = self.link_generator(pattern)
            res = self.post(url , chat_id )
            if res and res.status_code == 200 :
                res = Response(res.json())
                return res
            return None  
        
    

    def volume_change(self , chat_id ,operations_type , volume):
            pattern = 'volume_change'
            url = self.link_generator(pattern)
            res = requests.post(url , data = {'user' : chat_id , 'operation_type' : operations_type , 'size' : volume} , headers=self.headers)
            return res
        

    def link_generator(self  , pattern = None):
            if pattern is not None :
                end_point = self.url.rstrip('/') + f'/{self.username}/api/{pattern}/'
                return end_point
            return None
        


    def get(self , url):
            res = requests.get(url , headers=self.headers)
            print(res.text)
            return res

    

    def post(self ,url , chat_id , full_name = None  ):
            if full_name != None :
                res = requests.post(url , headers=self.headers , data = {'chat_id' : chat_id , 'full_name' : full_name})
                print(res.text)
                return res
            else :
                res = requests.post(url , headers=self.headers , data = {'chat_id' : chat_id })
                print(res.text)

                return res




class Response:
    
    def __init__(self, data):
            self.data = data
            if type(data) is dict:
                for key, value in data.items():
                    if isinstance(value, dict):
                        setattr(self, key, Response(value))
                    else:
                        setattr(self, key, value)
        

    def __str__(self) -> str:
            return str(self.data) 
        

    def __getattr__(self, attr):
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{attr}'")
        



connection = VidConnec(api_key=api_key , url=api_url , bot_username=bot_username)
