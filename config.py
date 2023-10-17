import os

class Config:
    API_ID = int(os.environ.get("API_ID", "26177237")) #Karışmayın
    API_HASH = os.environ.get("API_HASH", "6929515a9de7f855c81d4e64f6f3a4e9") #Karışmayın
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6326154616:AAHIio0zXiVdCAOpcfOQ5jaNmcFk6-lMh8g") #Botunuzun Tokenini Girin .  
    PLAYLIST_ID = os.environ.get("PLAYLIST_ID", "")
