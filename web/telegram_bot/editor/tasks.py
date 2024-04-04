from celery import Celery
from pyrogram import Client
import redis
import os 
from datetime import datetime
from ffmpeg_progress_yield import FfmpegProgress
import os
import redis
import time
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)
import json
import requests
import subprocess
from utils.connection import connection as con 
from dotenv import load_dotenv
import os

update_sec  = 1
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
    

r = redis.Redis(host='localhost', port=6379, db=0 ,decode_responses=True)



def progressbar(current, total , task_id=None ):
    try :
        percentage = current * 100 // total
        progress_bar = ""
        for i in range(20):
            if percentage >= (i + 1) * 5:progress_bar += "█"
            elif percentage >= i * 5 + 2:progress_bar += "▒"
            else:progress_bar += "░"
            date = datetime.now()
        progress_data = {'progress' : progress_bar ,'percentage' : percentage , 'text' :f"{progress_bar} {percentage} ",'date' : str(date) }
        if not r.exists(task_id):
            r.hmset(task_id, progress_data)
            progress_data['is_update'] = 'True'
        elif r.exists(task_id ):
            if int(float(r.hgetall(task_id)['percentage'])) != percentage :
                p = r.hgetall(task_id)
                last_pdate = datetime.strptime(p['date'], '%Y-%m-%d %H:%M:%S.%f')
                time_difference = date - last_pdate
                seconds_difference = time_difference.total_seconds()
                if int(seconds_difference) >= update_sec :
                    progress_data['is_update'] = 'True'
                    r.hmset(task_id, progress_data)
                else :
                    progress_data['is_update'] = 'Fasle'
            else :
                r.hmset(task_id, progress_data)
                progress_data['is_update'] = 'False'
        return progress_data
    
    except Exception as e : print('prosseccbar func' , str(e))








app = Celery('tasks' , backend='redis://localhost:6379/6' , broker='redis://localhost:6379/6')
app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json',],  
    worker_concurrency=3,
    worker_prefetch_multiplier=1,
)

session = '' # session string telegram bot 



@app.task(name='tasks.editor', bind=True, default_retry_delay=1)
def editor(self , files , viddata):
    try :
        user_files_data = files
        con = VidConnec(api_key=api_key, url=api_url, bot_username=bot_username)
        if con  and con.setting :setting =con.setting
        work_dir = 'workdir'
        base_dir = os.getcwd()
        task_id = self.request.id
        directory_name = str(task_id)
        full_path = os.path.join(work_dir, directory_name)
        os.makedirs(full_path, exist_ok=True)
        print(viddata)

        bot = Client('test'  , api_id=api_id , api_hash=api_hash , bot_token=bot_token  , session_string=session , proxy=proxy)

        
        def downloader(files):


            total_files = len(files)
            if total_files == 1 :
                file_1 = files[0]
                print(file_1)
                vid1 = f'{base_dir}/{work_dir}/{directory_name}/vid1.mp4'
                with bot :
                    msg = bot.get_messages(chat_id=int(file_1[0]) , message_ids=int(file_1[1]))
                    def progress(current, total):
                        data = int(float(f"{current * 100 / total:.1f}"))
                        progress = progressbar(data , 400 , str(task_id) )
                        if progress['is_update'] == 'True' :
                            pbar = progress['text']
                            text = f'عملیات در حال پردازش میباشد\n\n📥{str(pbar)}'
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                    bot.download_media(msg, progress=progress , file_name=vid1)


            elif total_files == 2 :
                file_1  = files[0]
                vid1 = f'{base_dir}/{work_dir}/{directory_name}/vid1.mp4'
                file_2 = files[1]
                vid2= f'{base_dir}/{work_dir}/{directory_name}/vid2.mp4'

                with bot :
                    msg = bot.get_messages(chat_id=int(file_1[0]) , message_ids=int(file_1[1]))
                    def progress(current, total):
                        data = int(float(f"{current * 100 / total:.1f}"))
                        progress = progressbar(int(data /2) , 400 , str(task_id) )
                        if progress['is_update'] == 'True' :
                            pbar = progress['text']
                            text = f'عملیات در حال پردازش میباشد\n\n📥{str(pbar)}'
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                    bot.download_media(msg, progress=progress , file_name=vid1)


                with bot :
                    msg = bot.get_messages(chat_id=int(file_2[0]) , message_ids=int(file_2[1]))
                    def progress(current, total):
                        data = int(float(f"{current * 100 / total:.1f}"))
                        progress = progressbar(int(data /2+50), 400 , str(task_id) )
                        if progress['is_update'] == 'True' :
                            pbar = progress['text']
                            text = f'عملیات در حال پردازش میباشد\n\n📥{str(pbar)}'
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                    bot.download_media(msg, progress=progress , file_name=vid2)




            elif total_files == 3 :
                file_1  = files[0]
                vid1= f'{base_dir}/{work_dir}/{directory_name}/vid1.mp4'
                file_2 = files[1]
                vid2= f'{base_dir}/{work_dir}/{directory_name}/vid2.mp4'
                file_3= files[2]
                vid3= f'{base_dir}/{work_dir}/{directory_name}/vid3.mp4'


                with bot :
                    msg = bot.get_messages(chat_id=int(file_1[0]) , message_ids=int(file_1[1]))
                    def progress(current, total):
                        data = int(float(f"{current * 100 / total:.1f}"))
                        progress = progressbar(int(data /3) , 400 , str(task_id) )
                        if progress['is_update'] == 'True' :
                            pbar = progress['text']
                            text = f'عملیات در حال پردازش میباشد\n\n📥{str(pbar)}'
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                    bot.download_media(msg, progress=progress , file_name=vid1)


                with bot :
                    msg = bot.get_messages(chat_id=int(file_2[0]) , message_ids=int(file_2[1]))
                    def progress(current, total):
                        data = int(float(f"{current * 100 / total:.1f}"))
                        progress = progressbar(int(data /3+33.33), 400 , str(task_id) )
                        if progress['is_update'] == 'True' :
                            pbar = progress['text']
                            text = f'عملیات در حال پردازش میباشد\n\n📥{str(pbar)}'
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                    bot.download_media(msg, progress=progress , file_name=vid2)

                with bot :
                    msg = bot.get_messages(chat_id=int(file_3[0]) , message_ids=int(file_3[1]))
                    def progress(current, total):
                        data = int(float(f"{current * 100 / total:.1f}"))
                        progress = progressbar(int(data /3+66.66), 400 , str(task_id) )
                        if progress['is_update'] == 'True' :
                            pbar = progress['text']
                            text = f'عملیات در حال پردازش میباشد\n\n📥{str(pbar)}'
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                    bot.download_media(msg, progress=progress , file_name=vid3)

            if viddata['thumbnail'] != 'None'  :
                    image_path= f'{base_dir}/{work_dir}/{directory_name}/image.jpeg'
                    with bot :
                        msg = bot.get_messages(chat_id=backup_channel , message_ids=int(viddata['thumbnail']))
                        bot.download_media(msg , file_name=image_path)
            elif viddata['vid_thumb'] != 'None' :
                image_path= f'{base_dir}/{work_dir}/{directory_name}/image.jpeg'
                with bot :
                    bot.download_media( viddata['vid_thumb'] , file_name=image_path)
                



        def videditor(files):

            
            main_path = f'{base_dir}/{work_dir}/{directory_name}/'
            image_path = f'{base_dir}/{work_dir}/{directory_name}/image.jpeg'
            print(files)
            if len(files) == 1:files = ['vid1']
            if len(files) == 2:files = ['vid1','vid2']
            if len(files) == 3:files = ['vid1','vid2','vid3']

            ff = FfmpegProgress(generate_ffmpeg_command(main_path = main_path, files=files , image_path=image_path, watermark= setting.watermark_text, bit=viddata['quality']))
            for progress in ff.run_command_with_progress():
                data = int(str(progress).split('.')[0])
        

                pbar = progressbar(data *2 +100 , 400 , str(task_id))
                pbar_text= pbar['text']
                if pbar['is_update'] == 'True' :
                    text = f'عملیات در حال پردازش میباشد\n\n🔮{str(pbar_text)}'
                    with bot :
                        try :
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                        except Exception as e :print(e)

        def uploader():
                with bot :
                    def progress(current, total):
                        data = int(float(f"{current * 100 / total:.1f}"))
                        progress = progressbar(data +300 , 402 , str(task_id) )
                        if progress['is_update'] == 'True' :
                            pbar = progress['text']
                            text = f'عملیات در حال پردازش میباشد\n\n📤{str(pbar)}'
                            call_data = f'cancel_vid:{str(task_id)}:{str(viddata["total_size"])}'
                            bot.edit_message_text(chat_id=int(viddata['chat_id']) ,text = text ,message_id = int(viddata['message_id']) ,
                        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=call_data)],]))
                    vid_name = 'output.mp4'
                    if viddata['name'] != 'None' :
                        vid_name = viddata['name'].replace(' ' , '-')
                        vid_name = f'{vid_name}.mp4'
                    data = vidinfo( f'{base_dir}/{work_dir}/{directory_name}/output.mp4')
                    if data :caption =  f'`TIME : {data["time"]}\nSIZE : {data["size"]}`\n\n@VidCompressBot'
                    else :caption = '@VidCompressBot'

                    if setting.restrict_saving_content :
                        bot.send_video(int(viddata['chat_id'])  , f'{base_dir}/{work_dir}/{directory_name}/output.mp4',
                                        progress=progress , file_name= vid_name , caption =caption , protect_content = True) 
                    else :
                        bot.send_video(int(viddata['chat_id'])  , f'{base_dir}/{work_dir}/{directory_name}/output.mp4',
                                        progress=progress , file_name= vid_name , caption =caption)

                    bot.delete_messages(chat_id=int(viddata['chat_id']) , message_ids=int(viddata['message_id']))

                

                    

        try :
            downloader(files=files)
            videditor(files = files)
            uploader()
            delet_dir(f'{base_dir}/{work_dir}/{directory_name}')
        except Exception as e :
            with bot :
                try:
                    bot.send_message(chat_id='accroot' , text = str(e))
                except :pass
            delet_dir(f'{base_dir}/{work_dir}/{directory_name}')
            # con.volume_change(viddata['chat_id'] , operations_type='decrease' , volume=viddata['total_size'])

    except Exception as e : print('edirot task ' , str(e))
    

def delet_dir(path):
    try :
        os.system(f"rm -rf {path}")
    except Exception as e : print('delete dir ' , str(e))
    



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
        
    

    def link_generator(self  , pattern = None):
            if pattern is not None :
                end_point = self.url.rstrip('/') + f'/{self.username}/api/{pattern}/'
                return end_point
            return None


    
    
    def volume_change(self , chat_id ,operations_type , volume):
            pattern = 'volume_change'
            url = self.link_generator(pattern)
            res = requests.post(url , data = {'user' : chat_id , 'operation_type' : operations_type , 'size' : volume} , headers=self.headers)
            return res
        

    def get(self , url):

        try :
            return requests.get(url , headers=self.headers)
        except Exception as e:
            return None 
    

    def post(self ,url , chat_id , full_name = None  ):
        try :
            if full_name != None :
                return requests.post(url , headers=self.headers , data = {'chat_id' : chat_id , 'full_name' : full_name})
            else :
                return requests.post(url , headers=self.headers , data = {'chat_id' : chat_id })
                
        except Exception as e :
            return None 



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
        
    








def vidinfo(path):
    file_size   = None 
    file_time = None 
    video_path = path
    command = ['ffmpeg', '-i', video_path]
    output = subprocess.Popen(command, stderr=subprocess.PIPE).communicate()[1]
    output = output.decode('utf-8')
    time_index = output.find("Duration: ")
    if time_index != -1:
        time_str = output[time_index + 10:time_index + 21]
        file_time = time_str
    bytes = os.path.getsize(path)
    
    if bytes < 1024:
        file_size = "{} bytes".format(bytes)
    elif bytes < 1024 * 1024:
        kilobytes = bytes / 1024
        file_size = "{:.2f} KB".format(kilobytes)
    elif bytes < 1024 * 1024 * 1024:
        megabytes = bytes / (1024 * 1024)
        file_size = "{:.2f} MB".format(megabytes)
    else:
        gigabytes = bytes / (1024 * 1024 * 1024)
        file_size = "{:.2f} GB".format(gigabytes)

    return {'size' : file_size , 'time' : file_time}



def generate_ffmpeg_command(main_path, files , image_path , watermark , bit):
    cmd = ['ffmpeg']
    inputs = []
    filter_complex = ''

    for i, file in enumerate(files):
        input_path = f'{main_path}{file}.mp4'
        inputs.append(f'-i')
        inputs.append(input_path)
        filter_complex += f'[{i}:v][{i}:a]'
    filter_complex += f'concat=n={len(files)}:v=1:a=1[concatenated];'
    filter_complex += f'[concatenated][{len(files)}:v]overlay=0:0:enable=\'between(t,0,0.1)\',drawtext=text=\'{"" if watermark is None else watermark}\':fontsize=30:fontcolor=yellow:x=(main_w-text_w-10):y=(main_h-text_h-10)'
    cmd += inputs
    cmd += [
        '-i', image_path,
        '-filter_complex', filter_complex,
        '-vsync', 'vfr' ,
        '-r', '15', '-b:v', f'{bit}k', '-b:a', '64k',
        f'{main_path}output.mp4']
    return cmd
