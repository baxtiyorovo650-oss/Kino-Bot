import telebot

TOKEN = "8983559216:AAGtq-RhXY4JArqP3cE8knE9Jjl7uzUy4GE"
bot = telebot.TeleBot(TOKEN)

# Kino kodlari bazasi
movies = {
    "1": {
        "title": "Avatar 2: Suv yo'li", 
        "description": "Fantastika, sarguzasht",
        "link": "https://t.me/kanal_ manzili yoki video_file_id"
    },
    "2": {
        "title": "Forsaj 10", 
        "description": "Jangari, Detektiv",
        "link": "https://t.me/kanal_ manzili yoki video_file_id"
    }
}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "🎬 Assalomu alaykum! Kino botimizga xush kelibsiz.\n\nKino kodini yuboring (masalan: **1** yoki **2**):", 
        parse_mode="Markdown"
    )

@bot.message_handler(func=lambda message: True)
def get_movie(message):
    code = message.text.strip()
    
    if code in movies:
        movie = movies[code]
        text = f"🎬 **Kino:** {movie['title']}\n📌 **Janr:** {movie['description']}\n\n🔗 **Ko'chirib olish / Ko'rish:** {movie['link']}"
        bot.send_message(message.chat.id, text, parse_mode="Markdown")
    else:
        bot.reply_to(message, "❌ Kechirasiz, bunday kodli kino topilmadi. Iltimos, to'g'ri kodni kiriting.")

print("Kino bot ishga tushdi...")
bot.infinity_polling()
