from pyrogram import Client   , filters
from utils import filters as f 
from config import connection
from utils import btn






@Client.on_message(filters.private & f.bot_not_active , group=0)
async def bot_not_active(client , message):
      con = connection()
      if con and con.setting :
            await client.send_message(message.from_user.id , text = con.setting.not_active_text)




@Client.on_message(filters.private & f.user_not_active , group=0)
async def user_not_active(client , message):
            con = connection()
            if con and con.setting :
                  await client.send_message(message.from_user.id , text = con.setting.user_not_active_text)

@Client.on_message(filters.private & f.not_join)
async def user_not_join(client , message ):
            con = connection()
            if con and con.setting and con.setting.join_channel_text and con.setting.channel_url:
                  await client.send_message(message.from_user.id , text = con.setting.join_channel_text ,
                                          reply_markup = btn.join_channel_link(con.setting.channel_url))
                  