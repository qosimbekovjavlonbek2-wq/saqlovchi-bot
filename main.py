import os
import telebot
from yt_dlp import YoutubeDL

# BotFather bergan tokenni shu yerga qo'yamiz
BOT_TOKEN = "8657528354:AAEMdekppz9W_LQ0g0D0uhWyAl8Bs7e7des"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Menga Instagram, TikTok yoki YouTube havolasini yuboring, men uni sizga yuklab beraman. Hech qanday obunalar talab qilinmaydi! 😎")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text
    
    # Havolani tekshirish
    if not ("instagram.com" in url or "tiktok.com" in url or "youtube.com" in url or "youtu.be" in url):
        bot.reply_to(message, "Iltimos, faqat Instagram, TikTok yoki YouTube havolasini yuboring. ⚠️")
        return

    status_msg = bot.reply_to(message, "Videoni yuklab olishni boshladim, kuting... ⏳")

    # Yuklab olish sozlamalari (Faqat bitta fayl qilib yuklash)
    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'best',
        'max_filesize': 45 * 1024 * 1024, # Telegram botlar uchun 45-50 MB gacha cheklov bor
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Agar fayl formati boshqacha bo'lsa, aniq nomini topamiz
            if not os.path.exists(filename):
                filename = "video.mp4" # default ko'rinish

        # Videoni foydalanuvchiga yuborish
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video, caption="Mana siz so'ragan video! 🎬\n\n@saqlovchiii_bot orqali yuklab olindi.")
        
        # Keraksiz faylni o'chirib tashlaymiz (Joy to'lmasligi uchun)
        os.remove(filename)
        bot.delete_message(message.chat.id, status_msg.message_id)

    except Exception as e:
        bot.edit_message_text(f"Xatolik yuz berdi yoki video hajmi juda katta: {str(e)}", message.chat.id, status_msg.message_id)
        if os.path.exists('video.mp4'): os.remove('video.mp4')

# Botni doimiy ishga tushirish
bot.infinity_polling()
