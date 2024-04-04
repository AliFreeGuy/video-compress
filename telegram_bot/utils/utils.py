import jdatetime


def jdate(date_miladi):
        try :date_time = jdatetime.datetime.strptime(date_miladi, "%Y-%m-%dT%H:%M:%S.%fZ")
        except : date_time = jdatetime.datetime.strptime(date_miladi, "%Y-%m-%dT%H:%M:%SZ")
        date_shamsi = jdatetime.datetime.fromgregorian(datetime=date_time).replace(hour=0, minute=0, second=0, microsecond=0)
        current_date_shamsi = jdatetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        remaining_days = (date_shamsi - current_date_shamsi).days
        date = date_shamsi.strftime('%Y-%m-%d').split('-')
        date = f'{date[2]}-{date[1]}-{date[0]}'
        print(date)
        result = {
            'date': date,
            'day': remaining_days
        }
        return result





def m_to_g(data):
        number = data
        result = number / 1000
        formatted_result = "{:.2f}".format(result)
        return formatted_result




def to_meg(number):
            megabytes = round(int(number) / 1_024 / 1_024)
            return megabytes

    

def g_to_m(data ):
        return int(data) * 1024
    
    



def vid_valid(vid ):
        files = []

        if vid.vid1 != 'None' :files.append('test')
        if vid.vid2 != 'None' :files.append('test')
        if vid.vid3 != 'None' :files.append('test')

        if files :
            return False
        return True
    
    

     

