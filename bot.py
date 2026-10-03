import os
import telebot
from google import genai

# 1. GitHub par token leak na ho, isliye isko generic rakha hai
# Render par environment variables mein 'TELEGRAM_BOT_TOKEN' aur 'GEMINI_API_KEY' add karna hoga
BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_TELEGRAM_BOT_TOKEN_HERE')
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', 'YOUR_GEMINI_API_KEY_HERE')

# 2. Aapka private Telegram User ID
ALLOWED_USER_ID = 8254317641

bot = telebot.TeleBot(BOT_TOKEN)
ai_client = genai.Client(api_key=GEMINI_API_KEY)

# Security Check: Sirf aapke message ka reply dene ke liye function
def is_authorized(message):
    return message.from_user.id == ALLOWED_USER_ID

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if not is_authorized(message):
        return
    bot.reply_to(message, "Hello Sachin! Main aapka private Gemini AI Assistant bot hoon. Poochhiye kya poochhna hai?")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if not is_authorized(message):
        return
    
    try:
        # User ke text message ko Gemini AI ke paas bhejna
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
        )
        # AI ka reply user ko send karna
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, f"Sorry, ek error aayi: {str(e)}")

if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
