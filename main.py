import telebot
from flask import Flask
import threading
import os

TOKEN = '8983559216:AAGtq-RhXY4JArqP3cE8knE9Jjl7uzUy4GE'
bot = telebot.TeleBot(TOKEN)
app = Flask('')

@app.route('/')
def home():
    return "Bot ishlayapti!"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Botimiz Render orqali 24/7 ishlamoqda! 🤖")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, f"Siz yozdingiz: {message.text}")

def run_flask():
    # Render taqdim etadigan portni avtomatik oladi (default 8080)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Veb-serverni alohida oqimda ishga tushiramiz
t = threading.Thread(target=run_flask)
t.start()

print("Bot ishga tushdi...")
bot.infinity_polling()
