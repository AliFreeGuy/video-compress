from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)
from utils import vid_data
from config import connection


def support_pv(username):
        mark= [InlineKeyboardButton(text = 'خرید از پشتیبانی'  ,url=f'https://t.me/{username}' ),],
        return InlineKeyboardMarkup(mark)


def video_panel(vid):
                con = connection()
                if con and con.setting :
                        setting = con.setting
                x  = vid
                marks = [
                
                        [
                                InlineKeyboardButton(text = f'{"✔️" if x.quality == str(setting.quality_3) else ""} کیفیت خوب'  ,callback_data=f'vid:q3:{str(setting.quality_3)}' ),
                                InlineKeyboardButton(text= f'{"✔️" if x.quality == str(setting.quality_2) else ""} کیفیت متوسط'  ,callback_data=f'vid:q2:{str(setting.quality_2)}' ),
                                InlineKeyboardButton(text= f'{"✔️" if x.quality == str(setting.quality_1) else ""} کیفیت کم'  ,callback_data=f'vid:q1:{str(setting.quality_1)}' ),
                        ],

        

                        [InlineKeyboardButton(text = f'{"✔️" if x.name != "None" else "➕"} نام ویدیو', callback_data=f'vid:name:{x.chat_id}'),
                        InlineKeyboardButton(text = f'{"✔️" if x.thumbnail != "None" else "➕"} ثامبنیل ویدیو', callback_data=f'vid:image:{x.chat_id}')],

                        
                        [
                                InlineKeyboardButton(text = f'{"✔️" if x.vid3 !="None" else "➕"} ویدیو 3', callback_data=f'vid:vid3:{x.chat_id}'),
                                InlineKeyboardButton(text = f'{"✔️" if x.vid2 !="None" else "➕"} ویدیو 2', callback_data=f'vid:vid2:{x.chat_id}'),
                                InlineKeyboardButton(text = f'{"✔️" if x.vid1 !="None" else "➕"} ویدیو 1', callback_data=f'vid:vid1:{x.chat_id}'),
                                
                        ],



                        [InlineKeyboardButton(text = 'شروع عملیات', callback_data=f'vid:start:{x.chat_id}')],


                        ]
                return InlineKeyboardMarkup(marks) 



def cancel_task_btn(task_id , file_size):
                return InlineKeyboardMarkup([[InlineKeyboardButton(text = 'لغو عملیات', callback_data=f'cancel_vid:{task_id}:{str(file_size)}')],])
      

def join_channel_link(url):
                return InlineKeyboardMarkup([[InlineKeyboardButton(text = 'عضویت در کانال', url=url)],])
      



def user_panel():
        marks = [
                
                ['🪄 ویدیو ادیتور 🪄'],['👤 حساب کاربری 👤'],
                ['🧑‍✈️ پشتیبانی','🆘 راهنما','🎫 اشتراک']
                ]

        return ReplyKeyboardMarkup(marks , resize_keyboard=True)

























































































































