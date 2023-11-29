import wget
import coroutine
import os, youtube_dl, requests, time

from youtube_search import YoutubeSearch

from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery 
from yt_dlp import YoutubeDL
import os, youtube_dl, requests, time
from config import Config
from youtube_search import YoutubeSearch
from pyrogram.handlers import MessageHandler
from pyrogram import Client, filters
import yt_dlp
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message
)


bot = Client(
    'goktugass',
    bot_token = Config.BOT_TOKEN,
    api_id = Config.API_ID,
    api_hash = Config.API_HASH
)

# START KOMUTU
@bot.on_message(filters.command(["start"]) & filters.private)
async def start_(client, message):
    chat_id = message.chat.id
    helptext = f'**📥 Telegram Müzik & Video İndirme Botudur, Tamamen Ücretsizdir ...\n\n» /bul < müzik adı >\n    - Anında Müzik İndirir ...\n» /vbul < video adı >\n    - Anında Video İndirir ...**'
    await client.send_message(
        chat_id,
        text=helptext,
        reply_markup=InlineKeyboardMarkup(
            [[
                    InlineKeyboardButton('✨ ʙᴇɴɪ ɢʀᴜʙᴀ ᴇᴋʟᴇ ', url=f'http://t.me/KurdDowlandsBot?startgroup=new'),
                  ],[
                    InlineKeyboardButton('💡 ᴋᴀɴᴀʟ', url=f'https://t.me/KurdMuzikFM')
                  ],[
                    InlineKeyboardButton('👨‍💻 ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ', url=f'https://t.me/J3llack')
                  ]
            ]
        )
    )
    
    first_name = message.from_user.mention
    user_id = message.from_user.id
    
    await client.send_message(-1002126216629, f"""
Özelden Start Verdi
Kullanıcı adı : {first_name}
Kullanıcı İD : {user_id}
"""
)   
    
# MÜZİK İNDİRME KOMUTU
@bot.on_message(filters.command(["bul", "song"]) & ~filters.edited)
async def bul(_, message):
    query = " ".join(message.command[1:])
    m = await message.reply("➻ **sᴀʀᴋɪ ᴀʀᴀɴɪʏᴏʀ ...**")
    ydl_ops = {"format": "bestaudio[ext=m4a]"}
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        kisi = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

        
        mel = f"👤 İstiyen [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n☁️ **Başlık :** [{title[:23]}]({link})\n⏱️ **Süre :** `{duration}`\n\n💠Yükleyen Bot : @DownloadMusiccBot"
    except Exception as e:
        await m.edit("➻ **şᴀʀᴋɪ ʙᴜʟᴜɴᴀᴍᴀᴅɪ ...🎶**")
        print(str(e))
        return
    await m.edit("➻ **şᴀʀᴋɪ ɪɴᴅɪʀɪʟɪʏᴏʀ ...🎶**")
    try:
        with yt_dlp.YoutubeDL(ydl_ops) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio_file = ydl.prepare_filename(info_dict)
            ydl.process_info(info_dict)
        rep = f"**👤 İstiyen [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n☁️ **Başlık :** [{title[:23]}]({link})\n⏱️ **Süre :** `{duration}\n\n**✨Müziğiniz Alttaki Kanalda Paylaşıldı..**\n\n@KurdMuzikFm"                                                
        res = f"**👤 İstiyen [{message.from_user.first_name}](tg://user?id={message.from_user.id})\n☁️ **Başlık :** [{title[:23]}]({link})\n⏱️ **Süre :** `{duration}\n\n**✨Müziğiniz Alttaki Kanalda Paylaşıldı.**\n\n@KurdMuzikFm"                                                           
        secmul, dur, dur_arr = 1, 0, duration.split(":")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(float(dur_arr[i])) * secmul
            secmul *= 60
        await m.edit("➻ **şᴀʀᴋɪ ʏᴜ̈ᴋʟᴇɴɪʏᴏʀ ...🎶**")
        await message.reply_audio(audio_file, caption=rep, parse_mode='md',quote=False, title=title, duration=dur, thumb=thumb_name, performer="@KurdDowlandsBot")
        await m.delete()
        await bot.send_audio(chat_id=-1001566400712, audio=audio_file, performer="@KurdowlandsBot", parse_mode='md', title=title, duration=dur, thumb=thumb_name, caption=mel)
    except Exception as e:
        await m.edit("🔺 **ʙᴇɴɪ ʏᴏɴᴇᴛɪᴄɪ ʏᴀᴘɪɴ ...**")
        print(e)

    try:
        os.remove(audio_file)
        os.remove(thumb_name)
    except Exception as e:
        print(e)


# VİDEO İNDİRME KOMUTU
@bot.on_message(
    filters.command(["vbul", "vsong"]) & ~filters.edited
)
async def vsong(client, message):
    ydl_opts = {
        "format": "best",
        "keepvideo": True,
        "prefer_ffmpeg": False,
        "geo_bypass": True,
        "outtmpl": "%(title)s.%(ext)s",
        "quite": True,
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("➻ **ᴠɪᴅᴇᴏ ᴀʀᴀɴɪʏᴏʀ ...🎶**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"➻ **ᴠɪᴅᴇᴏ ʙᴜʟᴜɴᴀᴍᴀᴅɪ ...🎶**")
    preview = wget.download(thumbnail)
    await msg.edit("➻ **ᴠɪᴅᴇᴏ ɪɴᴅɪʀɪʟɪʏᴏʀ ...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data["title"],
    )
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)



bot.run()
