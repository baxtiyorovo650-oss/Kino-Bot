import os
from flask import Flask, request
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

# Bot tokeningiz
TOKEN = "8983559216:AAGtq-RhXY4JArqP3cE8knE9Jjl7uzUy4GE"

# Majburiy obuna bo'lishi kerak bo'lgan 2 ta kanal
CHANNEL_1 = "@sarikazartnik1"
CHANNEL_2 = "@raisboy_viip"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


# 1. Ikkala kanal uchun obunani tekshiruvchi funksiya
def check_subscriptions(user_id):
  channels = [CHANNEL_1, CHANNEL_2]
  for channel in channels:
    try:
      member = bot.get_chat_member(chat_id=channel, user_id=user_id)
      # Agar foydalanuvchi kanalni tark etgan yoki chiqarib yuborilgan bo'lsa
      if member.status in ["left", "kicked"]:
        return False
    except Exception as e:
      print(f"Xatolik ({channel} uchun): {e}")
      # Agar bot kanalga admin qilinmagan bo'lsa yoki xatolik bo'lsa, xavfsizlik uchun False qaytaramiz
      return False
  return True


# 2. Start komandasi
@bot.message_handler(commands=["start"])
def send_welcome(message):
  user_id = message.from_user.id

  # Obunani tekshiramiz
  if not check_subscriptions(user_id):
    markup = InlineKeyboardMarkup()
    # 1-kanal uchun tugma
    btn_channel_1 = InlineKeyboardButton(
        text="📢 1-Kanalga obuna bo'lish",
        url=f"https://t.me/{CHANNEL_1.replace('@', '')}",
    )
    # 2-kanal uchun tugma
    btn_channel_2 = InlineKeyboardButton(
        text="📢 2-Kanalga obuna bo'lish",
        url=f"https://t.me/{CHANNEL_2.replace('@', '')}",
    )
    # Tekshirish tugmasi
    btn_check = InlineKeyboardButton(
        text="✅ Tekshirish", callback_data="check_sub"
    )

    markup.add(btn_channel_1)
    markup.add(btn_channel_2)
    markup.add(btn_check)

    bot.send_message(
        message.chat.id,
        "Botimizdan foydalanish uchun avval quyidagi **ikkala kanalimizga** ham obuna bo'ling:",
        reply_markup=markup,
        parse_mode="Markdown",
    )
  else:
    bot.reply_to(
        message,
        "Xush kelibsiz! Botimizdan bemalol foydalanishingiz mumkin.",
    )


# 3. Tekshirish tugmasi bosilganda
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback_check(call):
  user_id = call.from_user.id

  if check_subscriptions(user_id):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    bot.send_message(
        call.message.chat.id,
        "Rahmat! Ikkala kanalga ham obuna tasdiqlandi. Endi botdan foydalanishingiz mumkin.",
    )
  else:
    bot.answer_callback_query(
        call.id,
        "Siz hali hamma kanallarga obuna bo'lmadingiz! ❌",
        show_alert=True,
    )


# 4. Flask Webhook qismi (Render uchun)
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
  json_string = request.get_data().decode("utf-8")
  update = telebot.types.Update.de_json(json_string)
  bot.process_new_updates([update])
  return "!", 200


@app.route("/")
def index():
  return "Bot is running 24/7!"


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

