from pyrogram import Client   , filters
from utils import filters as f 
from config import connection
from utils import text , btn
from editor.tasks import editor



@Client.on_message(filters.private & f.bot_is_active & f.user_is_active & f.is_join , group=1 )
async def base_command_handler(client , message ):
        con = connection()
        if message and message.text and con and con.setting :

            if message.text == '/help' or message.text == '🆘 راهنما':
                await client.send_message(message.from_user.id  , text = con.setting.help_text)
            
            elif message.text == '/start'  :

                await client.send_message(message.from_user.id  , text = con.setting.start_text , reply_markup = btn.user_panel())

            elif message.text == '/support'or message.text == '🧑‍✈️ پشتیبانی' :
                await client.send_message(message.from_user.id  , text = con.setting.support_text)

            elif message.text == '/profile' or message.text == '👤 حساب کاربری 👤':
                await user_profile(client , message)

            elif message.text == '/plans'or message.text == '🎫 اشتراک' :
                await plans_manager(client , message)
    

        



async def user_profile(client , message  ):
    con = connection()
    if con :
        user = con.get_user(chat_id=message.from_user.id)
        if user :
            plans = con.plans
            await client.send_message(chat_id = message.from_user.id  , text = text.user_profile_data(user = user , plans = plans))

async def plans_manager(client , message ):
    con = connection()
    if con :
        support_username =con.setting.support_id 
        plans = con.plans
        if len(plans)  == 0 :await client.send_message(message.from_user.id , text =text.plan_not_found(support_username))
        else :await client.send_message(message.from_user.id , text = text.plan_information(con.plans) , reply_markup = btn.support_pv(support_username))
                



