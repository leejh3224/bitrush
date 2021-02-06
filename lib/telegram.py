import os
import telegram

access_token = os.getenv("BITRUSH_BOT_ACCESS_TOKEN")
chat_id = os.getenv("BITRUSH_BOT_CHAT_ID")

bot = telegram.Bot(token=access_token)


def send_message(text):
    bot.send_message(chat_id, text=text)
