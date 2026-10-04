import os
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from flask import Flask, request

TOKEN = os.environ.get('BOT_TOKEN', '8983559216:AAGtq-RhXY4JArqP3cE8knE9Jjl7uzUy4GE')
CHANNEL_ID = '@kanal_username'  # <-- O'z kanalingiz userini yozing (masalan: @mening_kanalim)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# --- 1. Obunani tekshiruvchi funksiya ---
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        if member.status in ['left', 'kicked']:
            return False
        return True
    except Exception as e:
        print(f"Xatolik: {e}")
        return False


# --- 2. Start komandasi (Obuna tekshiruvi bilan) ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if not check_subscription(user_id):
        # Obuna bo'lmasa tugma chiqaramiz
        markup = InlineKeyboardMarkup()
        btn_channel = InlineKeyboardButton(
            text="📢 Kanalga obuna bo'lish",
            url=f"https://t.me/{CHANNEL_ID.replace('@', '')}"
        )
        btn_check = InlineKeyboardButton(
            text="✅ Tekshirish", 
            callback_data="check_sub"
        )
        markup.add(btn_channel)
        markup.add(btn_check)
        
        bot.send_message(
            message.chat.id,
            "Botimizdan foydalanish uchun avval quyidagi kanalimizga obuna bo'ling:",
            reply_markup=markup
        )
    else:
        # Obuna bo'lgan bo'lsa
        bot.reply_to(message, "Xush kelibsiz! Botimizdan bemalol foydalanishingiz mumkin.")


# --- 3. Tekshirish tugmasi bosilganda ---
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
    user_id = call.from_user.id
    
    if check_subscription(user_id):
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(
            call.message.chat.id,
            "Rahmat! Obuna tasdiqlandi. Endi botdan foydalanishingiz mumkin."
        )
    else:
        bot.answer_callback_query(
            call.id,
            "Siz hali kanalga obuna bo'lmadingiz! ❌",
            show_alert=True
        )


# --- Flask Webhook qismi (Sizda qanday bo'lsa, o'shancha qoldirasiz) ---
@app.route(f'/{TOKEN}', methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
