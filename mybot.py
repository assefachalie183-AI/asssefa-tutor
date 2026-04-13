import os
import telebot
import google.generativeai as genai

# ቶከኖችን ከ Environment Variables መውሰድ
TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = os.environ.get('GEMINI_API_KEY')

# Gemini ማዋቀር (ወደ አዲሱ gemini-1.5-flash ተቀይሯል)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "ሰላም Assefa! ቦቱ አሁን በአዲሱ ሞዴል መስራት ጀምሯል። ጥያቄህን መጠየቅ ትችላለህ።")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "ይቅርታ፣ ችግር አጋጥሞኛል። እባክህ ትንሽ ቆይተህ ሞክር።")

print("ቦቱ ዝግጁ ነው...")
bot.infinity_polling()
