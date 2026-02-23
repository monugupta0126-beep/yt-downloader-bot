import telebot
import os
from yt_dlp import YoutubeDL

# Render par hum TOKEN ko environment variable se uthayenge
API_TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Render Par Live! YouTube link bhejein (480p Download):")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status = bot.reply_to(message, "⏳ High Quality 480p fetch ho raha hai...")
        file_name = "video.mp4"
        
        ydl_opts = {
            'format': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]/best',
            'outtmpl': file_name,
            'merge_output_format': 'mp4',
            'quiet': True,
        }
        
        try:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open(file_name, 'rb') as video:
                bot.send_video(message.chat.id, video, caption="🎬 Done by Render Bot")
            
            os.remove(file_name)
            bot.delete_message(message.chat.id, status.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, status.message_id)
    else:
        bot.reply_to(message, "Sahi link bhejo!")

# Render par bot ko chalu rakhne ke liye polling
bot.polling(none_stop=True)

