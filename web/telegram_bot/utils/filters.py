from pyrogram import filters
from config import connection
from utils import text
from utils.vid_data import save_message

async def bot_is_active(_ , __ , msg):
        if int(msg.id) < 1000000:
            await save_message(chat_id=msg.from_user.id , message_id=msg.id)
        con  = connection()
        
        if con and con.setting:
            if con.setting.is_active :
                return True
        return False
    




async def bot_not_active(_ , __ , msg ):
        con = connection()
        if con and con.setting :
            if con.setting.is_active == False:
                return True
            else:return False
        return True
    





async def user_not_active(_ , __ , msg ):
        con = connection()
        if con :
            first_name = str(msg.from_user.first_name if msg.from_user.first_name is not None else '')
            last_name = str(msg.from_user.last_name if msg.from_user.last_name is not None else '')
            full_name =  f'{str(first_name)} {str(last_name)}'
            chat_id  = int(msg.from_user.id )
            user = con.user(chat_id=chat_id , full_name=full_name)
            if user and user.is_active is False :
                return True
            else :return False
        return False
    
        
async def user_is_active(_ , __ , msg ):
        con = connection()
        if con :
            first_name = str(msg.from_user.first_name if msg.from_user.first_name is not None else '')
            last_name = str(msg.from_user.last_name if msg.from_user.last_name is not None else '')
            full_name =  f'{str(first_name)} {str(last_name)}'
            chat_id  = int(msg.from_user.id )
            user = con.user(chat_id=chat_id , full_name=full_name)
            if user and user.is_active :
                return True
            else :return False
        return False
    



async def is_join(_ , cli , msg ):
        con = connection()
        if con and con.setting :
            if con.setting.channel_chat_id  != None :
                try :
                    await cli.get_chat_member(con.setting.channel_chat_id, msg.from_user.id)
                    return True
                except Exception as e :
                    return False
            else:return True
        return False
    


async def not_join(_ , cli , msg ):
        con = connection()
        if con and con.setting :
            if con.setting.channel_chat_id  != None :
                try :
                    await cli.get_chat_member(con.setting.channel_chat_id, msg.from_user.id)
                    return False
                except Exception as e :
                    return True
            else:return False
        return False
    


user_is_active = filters.create(user_is_active)
user_not_active =filters.create(user_not_active)
bot_not_active = filters.create(bot_not_active)
bot_is_active = filters.create(bot_is_active)
is_join = filters.create(is_join)
not_join = filters.create(not_join)
