import openai
import os
import json
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackQueryHandler, Application
from queue import Queue


openai.api_key = os.environ["OPENAI_API_KEY"]

def start(update, context):
    update.message.reply_text("Welcome! You can control the temperature of the generated text by using the /temperature command.")

def temperature(update, context):
    try:
        temperature = float(context.args[0])
        if temperature < 0 or temperature > 1:
            raise ValueError
        context.bot.temperature = temperature
        update.message.reply_text(f"Temperature set to {temperature}")
    except (ValueError, IndexError):
        update.message.reply_text("Please input a valid temperature value between 0 and 1.")

def generate_text(update, context):
    try:
        prompt = (f"textgen {update.message.text}")
        completions = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=context.bot.temperature,
            max_tokens=1024
        )
        message = completions.choices[0].text
        update.message.reply_text(message)
    except openai.exceptions.OpenAiError as e:
        update.message.reply_text(str(e))

def main():
    application = Application.builder().token("TELEGRAM_BOT_TOKEN").build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        TEMPERATURE: [CommandHandler("temperature", temperature)],
        TEXT: [MessageHandler(Filters.text, generate_text)],
    )
    application.add_handler(conv_handler)
    application.run_polling()
    application.idle()
    

if __name__ == '__main__':
    main()
