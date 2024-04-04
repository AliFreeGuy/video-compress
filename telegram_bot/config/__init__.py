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
    



def connection():
    return con


