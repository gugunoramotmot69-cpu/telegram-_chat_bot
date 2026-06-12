import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# API Keys တွေကို Environment Variable ကနေ ဖတ်မယ်
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
TOKEN = os.environ.get("TELEGRAM_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! ကျွန်တော်က AI Bot ပါ။ ဘာများ ကူညီပေးရမလဲ?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # ChatGPT ဆီ စာပို့မယ်
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_text}]
    )
    
    bot_reply = response.choices[0].message.content
    await update.message.reply_text(bot_reply)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    application.run_polling()
