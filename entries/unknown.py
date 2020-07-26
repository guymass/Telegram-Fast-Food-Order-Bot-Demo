from lib import deco
from telegram.ext import Filters

@deco.run_async
@deco.global_message_handler(Filters.command)
def unknown(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text=" סליחה אבל הפקודה הזאת אינה מוכרת לי\nאנא כתבו את הפקודה /help בכדי לקבל רשימת הפקודות האפשריות.\n")
