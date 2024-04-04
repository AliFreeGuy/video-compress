from datetime import datetime
from utils.utils import jdate , m_to_g , to_meg


def user_profile_data(user  , plans ):

    try :
        text = []
        if user.sub.is_active  :
            text.append(f'آیدی اختصاصی : `{str(user.chat_id)}`')
            for plan in plans :
                if plan['id'] == user.sub.plan :
                    user_plan = plan 
                    text.append(f'اشتراک فعال : `{user_plan["name"]}`')
                    break
            text.append(f'حجم قابل استفاده : `{str(m_to_g(user.sub.volum))} گیگ`')
            text.append(f'حجم استفاده شده : `{str(m_to_g(user.sub.volum_used))} گیگ`')
            text.append(f'تاریخ پایان اشتراک : `{jdate(user.sub.expiry)["date"]}`')
            text.append('\nبرای ارتقا اشتراک بر روی /plans بزنید')

            return '\n'.join(text)
        
        else :
            return f'''
آیدی اختصاصی : `{str(user.chat_id)}`
اشتراک فعال : `خالی`

برای فعال سازی اشتراک بر روی /plans بزنید
        '''


    except Exception as e :
        print('user profile data text  ' , str(e))

        return 'خطایی پیش امده لطفا با پشتیبانی در تماس باشید /support'







def plan_not_found(support_username):
        return f'پلنی یافت نشد لطفا با ادمین در ارتباط باشید : @{support_username}'



def plan_information(plans):
        text = []
        for plan in plans:
            data = f'''
    پلن : `{plan['name']}`
    مدت قابل استفاده : `{str(plan['day'])} روز`
    حجم قابل استفاده : `{m_to_g(int(plan['volum']))} گیگ`
    توضیحات : `{plan['des']}`
    قیمت : `{plan['price']} هزارتومان`'''
            text.append(data)
        text.append('\nجهت خرید پلن مورد نظر خود از طریق دکمه زیر با پشتیبانی در ارتباط باشید')
        return '\n'.join(text)
    





def user_not_join(url ):
    
        if url != None :
            if not url.startswith('@') and not url.startswith('https://t.me/'):
                url = f'@{url}'
            else :url = url 
        else : url = 'خالی'

        text = f'''
    کاربر عزیز برای استفاده از امکانات این ربات باید در کانال اصلی ما به ادرس {str(url)} عضو شوید . بعد از عضویت به ربات برگشته و دستور /start ارسال کنید .
    '''
        
        return text
    




def vid_data_text(vid , setting = None  ):
    
    


    try :
        if vid is not None and setting is not None  :
            if vid.quality != 'None' :
                if int(vid.quality) == int(setting.quality_1):
                    quality = 'کم'
                elif int(vid.quality) == int(setting.quality_2):
                    quality = 'متوسط'
                elif int(vid.quality) == int(setting.quality_3):
                    quality = 'خوب'
            else : quality = 'خالی'

        else :
            quality = 'خالی'
        



        text = f'''
کیفیت : `{quality}`
نام : `{"خالی" if vid.name == "None" else vid.name}`
ثامبنیل : `{"خالی" if vid.thumbnail == "None" else "انتخاب شده"}`
ویدیو 1: `{"خالی" if vid.vidvol1 == "None" else f"{str(to_meg(vid.vidvol1))} مگابایت"}`
ویدیو 2: `{"خالی" if vid.vidvol2 == "None" else f"{str(to_meg(vid.vidvol2))} مگابایت"}`
ویدیو 3 : `{"خالی" if vid.vidvol3 == "None" else f"{str(to_meg(vid.vidvol3))} مگابایت"}`

برای راهنمایی و آموزش کار کردن با این ربات و اطلاعات بیشتر بر روی /help بزنید
    '''
        return text

    except Exception as e : print('vid data text ' , str(e))





error_text = 'خطا لطفا دوباره تلاش کنید !'
operationـhasـexpired =  'خطا این عملیات منقضی شده است لطفا دوباره تلاش کنید !'
send_name = 'نام ویدیو را ارسال کنید :'
send_thumbnail = 'تصویر ثامبنیل خود را ارسال کنید :'
send_video = 'ویدیو خود را ارسال کنید :'
