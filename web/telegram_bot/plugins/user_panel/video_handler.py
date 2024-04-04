from pyrogram import Client   , filters
from utils import filters as f 
from config import connection , backup_channel
from utils import text , btn 
from utils.utils import to_meg , vid_valid, m_to_g  , g_to_m 
from editor.tasks import editor
from utils import vid_data 
import random
from celery.result import AsyncResult
from utils.message_saver import get_messages
from utils.vid_data import save_message
from pyromod.exceptions import ListenerTimeout

@Client.on_message(filters.private & f.bot_is_active & f.user_is_active &f.is_join, group=2 )
async def video_manager(client , message ):





        if message.text and message.text == '/editor' or message.text and message.text =='🪄 ویدیو ادیتور 🪄'  :
            await vid_data.addvid(chat_id=message.from_user.id)
            vid = await vid_data.getvid(chat_id=message.from_user.id )
            msg = await client.send_message(chat_id = message.from_user.id, text = text.vid_data_text(vid) , reply_markup =btn.video_panel(vid))
            await vid_data.updatevid(chat_id=message.from_user.id , key='message_id' , val=msg.id)

    

@Client.on_callback_query(f.user_is_active &f.is_join & f.bot_is_active)
async def call_video_manager(client , call ):


        if call.data.startswith('vid:'):
            await vid_control(client , call )

        elif call.data.startswith('cancel_vid'):
            await cancel_vid(client , call )

        
    



    


async def vid_control(client , call ):
        vid = await vid_data.getvid(chat_id=call.from_user.id)
        if call.message.id == int(vid.message_id ) :
            con = connection()
            if con and con.setting :
                setting = con.setting
            status = call.data.split(':')[1]
            chat_id = call.from_user.id 
            call_val = call.data.split(':')[2]

            

            if status == 'q1':
                vid =await vid_data.getvid(chat_id)
                if vid.quality  == str(setting.quality_1) :await vid_data.updatevid(chat_id=chat_id , key='quality' , val='None')
                else :await vid_data.updatevid(chat_id=chat_id , key='quality' , val=call_val)
                await vid_updater(client , call)

                

            elif status == 'q2':
                vid =await vid_data.getvid(chat_id)
                if vid.quality  == str(setting.quality_2) :await vid_data.updatevid(chat_id=chat_id , key='quality' , val='None')
                else :await vid_data.updatevid(chat_id=chat_id , key='quality' , val=call_val)

                await vid_updater(client , call)


            elif status == 'q3':
                vid =await vid_data.getvid(chat_id)
                if vid.quality  == str(setting.quality_3) :await vid_data.updatevid(chat_id=chat_id , key='quality' , val='None')
                else :await vid_data.updatevid(chat_id=chat_id , key='quality' , val=call_val)
                await vid_updater(client , call)



            elif status == 'name' :
                vid = await vid_data.getvid(chat_id=call.from_user.id)
                if vid.name != 'None' :
                    await vid_data.updatevid(chat_id=call.from_user.id , key='name' , val='None')





                else :
                        await vid_deleter(client , call )
                        try :
                            ask = await client.ask(call.from_user.id , text.send_name , timeout = 60)
                        except ListenerTimeout:pass
                             
                        await save_message(chat_id=ask.from_user.id , message_id=ask.id)
                        if ask  :
                                if ask.text :
                                    await vid_data.updatevid(chat_id=call.from_user.id , key='name' , val=ask.text[:30])
                                else :
                                    await vid_deleter(client , call )
                                    await alert(client , call )
                        else :
                            await vid_deleter(client , call)
                            await alert(client , call )

                await vid_deleter(client , call)
                await vid_updater(client , call )
                
            elif status == 'image' :
                vid = await vid_data.getvid(chat_id=call.from_user.id )
                if vid.thumbnail != 'None' :
                    await vid_data.updatevid(chat_id=call.from_user.id , key='thumbnail' , val='None')
                else :
                        await vid_deleter(client , call )
                        try :
                            ask = await client.ask(call.from_user.id , text.send_thumbnail , timeout = 60)
                        except ListenerTimeout:pass

                        await save_message(chat_id=ask.from_user.id , message_id=ask.id)
                        if ask  :
                                if ask.photo :
                                    vid_backup = await client.send_photo(backup_channel , ask.photo.file_id)
                                    await vid_data.updatevid(chat_id=call.from_user.id , key='thumbnail' , val=vid_backup.id)
                                else :
                                    await vid_deleter(client , call )
                                    await alert(client , call )
                        else :
                            await vid_deleter(client , call)
                            await alert(client , call )
                await vid_deleter(client , call)
                await vid_updater(client , call )



            elif status == 'vid1' :
                con = connection()
                setting = None
                if con and con.setting :
                    setting = con.setting
                vid = await vid_data.getvid(chat_id=call.from_user.id )
                if vid.vid1 != "None":
                        await vid_data.updatevid(chat_id=call.from_user.id , key='vid1' , val='None')
                        await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol1' , val='None')
                
                
                else :
                        await vid_deleter(client , call )
                        try :
                            ask = await client.ask(call.from_user.id , text.send_video , timeout = 60)
                        except ListenerTimeout:pass
                        
                        await save_message(chat_id=ask.from_user.id , message_id=ask.id)
                        if ask  :
                                if ask.video :
                                    print(ask)
                                    if not vid_valid(vid = await vid_data.getvid(call.from_user.id)):
                                        file_size = int(to_meg(int(ask.video.file_size)))
                                        if setting != None and setting.video_limit > file_size :
                                            vid_backup = await client.send_video(backup_channel , ask.video.file_id , caption=f"`{str(ask.from_user.id)}` - `{str(ask.from_user.first_name)}`")
                                            await vid_data.updatevid(chat_id=call.from_user.id , key='vid1' , val=vid_backup.id)
                                            await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol1' , val=ask.video.file_size)
                                        else : await alert(client, call , msg=f'خطا حجم این ویدیو باید کمتر از {str(setting.video_limit)} مگابایت باشه !')
                                    else : 
                                        vid_backup = await client.send_video(backup_channel , ask.video.file_id , caption=f"`{str(ask.from_user.id)}` - `{str(ask.from_user.first_name)}`")
                                        await vid_data.updatevid(chat_id=call.from_user.id , key='vid1' , val=vid_backup.id)
                                        await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol1' , val=ask.video.file_size)
                                else :pass
                        else :pass
                            
                await vid_deleter(client , call)
                await vid_updater(client , call )

            elif status == 'vid2' :
                con = connection()
                setting = None
                if con and con.setting :
                    setting = con.setting
                

            
                vid = await vid_data.getvid(chat_id=call.from_user.id )
                if vid.vid2 != "None":
                        
                        await vid_data.updatevid(chat_id=call.from_user.id , key='vid2' , val='None')
                        await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol2' , val='None')
                
                
                else :
                        await vid_deleter(client , call )
                        try :
                            ask = await client.ask(call.from_user.id , text.send_video , timeout = 60)
                        except ListenerTimeout:pass
                        
                        await save_message(chat_id=ask.from_user.id , message_id=ask.id)
                        if ask  :
                                if ask.video :
                                    if not vid_valid(vid = await vid_data.getvid(call.from_user.id)):
                                        file_size = int(to_meg(int(ask.video.file_size)))
                                        if setting != None and setting.video_limit > file_size :
                                            vid_backup = await client.send_video(backup_channel , ask.video.file_id , caption=f"`{str(ask.from_user.id)}` - `{str(ask.from_user.first_name)}`")
                                            await vid_data.updatevid(chat_id=call.from_user.id , key='vid2' , val=vid_backup.id)
                                            await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol2' , val=ask.video.file_size)
                                        else : await alert(client, call , msg=f'خطا حجم این ویدیو باید کمتر از {str(setting.video_limit)} مگابایت باشه !')
                                    else : 
                                        vid_backup = await client.send_video(backup_channel , ask.video.file_id , caption=f"`{str(ask.from_user.id)}` - `{str(ask.from_user.first_name)}`")
                                        await vid_data.updatevid(chat_id=call.from_user.id , key='vid2' , val=vid_backup.id)
                                        await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol2' , val=ask.video.file_size)
                                else :pass
                                    
                        else : pass
                await vid_deleter(client , call)
                await vid_updater(client , call )


            elif status == 'vid3' :
                con = connection()
                setting = None
                if con and con.setting :
                    setting = con.setting


                vid = await vid_data.getvid(chat_id=call.from_user.id )
                if vid.vid3 != "None":
                        await vid_data.updatevid(chat_id=call.from_user.id , key='vid3' , val='None')
                        await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol3' , val='None')
                else :
                        await vid_deleter(client , call )
                        try :
                            ask = await client.ask(call.from_user.id , text.send_video , timeout = 60)
                        except ListenerTimeout:pass
                        
                        await save_message(chat_id=ask.from_user.id , message_id=ask.id)
                        if ask  :
                                if ask.video :
                                    if not vid_valid(vid = await vid_data.getvid(call.from_user.id)):
                                        file_size = int(to_meg(int(ask.video.file_size)))
                                        if setting != None and setting.video_limit > file_size :
                                            vid_backup = await client.send_video(backup_channel , ask.video.file_id , caption=f"`{str(ask.from_user.id)}` - `{str(ask.from_user.first_name)}`")
                                            await vid_data.updatevid(chat_id=call.from_user.id , key='vid3' , val=vid_backup.id)
                                            await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol3' , val=ask.video.file_size)
                                        else : await alert(client, call , msg=f'خطا حجم این ویدیو باید کمتر از {str(setting.video_limit)} مگابایت باشه !')
                                    else : 
                                        vid_backup = await client.send_video(backup_channel , ask.video.file_id , caption=f"`{str(ask.from_user.id)}` - `{str(ask.from_user.first_name)}`")
                                        await vid_data.updatevid(chat_id=call.from_user.id , key='vid3' , val=vid_backup.id)
                                        await vid_data.updatevid(chat_id=call.from_user.id , key='vidvol3' , val=ask.video.file_size)
                                else :pass
                                    
                        else : pass
                await vid_deleter(client , call)
                await vid_updater(client , call )

            





            elif status == 'start' :
                con = connection()
                setting = None
                if con and con.setting :setting = con.setting
                user = con.get_user(call.from_user.id )
                user_vid = await vid_data.getvid(call.from_user.id )

                validators = []
                files = []
                user_files = []


                if user_vid.vidvol1 != 'None' :
                    files.append(to_meg(int(user_vid.vidvol1)))
                    user_files.append([backup_channel,int(user_vid.vid1)])
                if user_vid.vidvol2 != 'None' :
                    files.append(to_meg(int(user_vid.vidvol2)))
                    user_files.append([backup_channel,int(user_vid.vid2)])
                if user_vid.vidvol3 != 'None' :
                    files.append(to_meg(int(user_vid.vidvol3)))
                    user_files.append([backup_channel,int(user_vid.vid3)])


                

                vid = await vid_data.getvid(chat_id=call.from_user.id )
                if not user.sub.is_active :validators.append('شما اشتراکی ندارید لطفا ابتدا اشتراک تهیه کنید')
                if not files :validators.append('برایه ادامه باید حدقل یک ویدیو انتخاب کرده باشید')
                if files and user_vid.quality == 'None' :validators.append('لطفا کیفیت ویدیو را انتخاب کنید')
                if user.sub.is_active :
                    user_volum = user.sub.volum - user.sub.volum_used
                    sub_checker = user_volum - sum(files)
                    if sub_checker < 0 :validators.append('حجم اشتراک شما برای این عملیات کم است')

                

                if validators :await alert(client , call , msg=validators[0])



                data = {
                                'name' : user_vid.name ,
                                'thumbnail' : user_vid.thumbnail ,
                                'quality' : user_vid.quality ,
                                'message_id' : call.message.id,
                                'chat_id'  :int(user_vid.chat_id) , 
                                'vid_thumb' : "None" , 
                                'total_size' : 0
                        }
                if not validators :
                    msg_id = user_files[0][1]
                    vid_thumb = await client.get_messages(backup_channel , msg_id)
                    if vid_thumb :data['vid_thumb'] = vid_thumb.video.thumbs[0].file_id
                    
                    changevolume= con.volume_change(chat_id=call.from_user.id , operations_type='increase' , volume=int(sum(files)))
                    print(changevolume)
                    if changevolume.status_code == 200 :
                        data['total_size'] = int(sum(files))
                        result = editor.apply_async(args=[user_files, data])
                        print(result)
                        await call.edit_message_text(text = 'در حال بارگذاری ...' , reply_markup= btn.cancel_task_btn(task_id=result ,file_size=sum(files)))
                    else :alert(client , call , msg='حجم اشتراک شما کم است')


        else : await alert(client , call , msg =text.operationـhasـexpired)








async def cancel_vid(client , call ):
        con = connection()
        file_size = int(call.data.split(':')[2])
        data = con.volume_change(chat_id=call.from_user.id , operations_type='decrease' , volume=file_size)
        print(data.text)
        print(call.data)
        task_id = call.data.split(":")[1]
        task = AsyncResult(task_id)
        task.revoke(terminate=True)
        await alert(client  ,call , msg= 'عملیات با موفقیت کنسل شد')
        await client.delete_messages(call.from_user.id , call.message.id)







async def alert(client ,call , msg = None ):
        if msg is None : await call.answer(text.error_text, show_alert=True)
        else : await call.answer(msg , show_alert = True)
    


async def vid_updater(client ,call  ):
        con = connection()
        setting = con.setting
        try :
            vid = await vid_data.getvid(chat_id=call.from_user.id )
            await call.edit_message_text(text =text.vid_data_text(vid , setting) , reply_markup = btn.video_panel(vid) )
        except Exception as e :
            print(e)
    



async def vid_deleter(client , call ):
        msg_id = call.message.id
        user_message_ids = get_messages(call.from_user.id )
        msgs = []
        for i in user_message_ids :
            if int(i)> int(msg_id):
                msgs.append(i)
                msgs.append(i+1)
                msgs.append(i-1)

        try :
            await client.delete_messages(call.from_user.id , msgs)
        except :return False






    




    











