import telebot
import os
from yt_dlp import YoutubeDL
from flask import Flask
from threading import Thread

# 1. Render ko zinda rakhne ke liye Web Server
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    # Render port 10000 use karta hai default mein
    app.run(host='0.0.0.0', port=10000)

# 2. Aapka Token yahan direct add kar diya hai
API_TOKEN = '8753514994:AAGbwCwus8v7KBeNHN6tXW2cZIE7vLXXCX8'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "✅ Render Par Live! YouTube link bhejein (480p Download):")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    if "youtube.com" in url or "youtu.be" in url:
        status = bot.reply_to(message, "⏳ Video fetch ho rahi hai (480p)...")
        # Unique file name taaki multiple users handle ho sakein
        file_name = f"video_{message.chat.id}.mp4"
        
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
                bot.send_video(message.chat.id, video, caption="🎬 Downloaded via Render Bot")
            
            if os.path.exists(file_name):
                os.remove(file_name)
            bot.delete_message(message.chat.id, status.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, status.message_id)
    else:
        bot.reply_to(message, "Bhai, sahi YouTube link toh bhejo!")

# 3. Bot aur Server ko saath mein chalane ka function
def start_bot():
    bot.polling(none_stop=True)

if __name__ == "__main__":
    # Server ko background thread mein chalayenge
    t = Thread(target=run)
    t.start()
    # Main thread mein bot chalega
    start_bot()
    
