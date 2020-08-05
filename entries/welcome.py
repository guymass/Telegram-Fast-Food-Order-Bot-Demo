from telegram.ext import (Filters, ConversationHandler)
from lib import deco
from lib.database import db

@deco.run_async
@deco.conversation_message_handler(Filters.status_update.new_chat_members)
def welcome(update, context):
    query = update.callback_query
    res = db.logo.find_one({"ImageCode":"logo"})
    url = res['ImageId']

    if context.user_data['fullname'] != "":
        fullname = context.user_data['fullname']
    else:
        firstName = update.effective_message.from_user.first_name
        lastName = update.effective_message.from_user.last_name
        fullname = str(firstName) #+ " " +  str(lastName)

    category = context.user_data
    reply_text = " \U0001F354 ברוכים הבאים {}\n  להתחלה לחצו על <b>/Start</b>\n".format(fullname)
    """star_keyboard = []
    star_keyboard =  [[InlineKeyboardButton("התחל", callback_data="restart")]]
    star_keyboard = list(star_keyboard)
    reply_markup_start = InlineKeyboardMarkup(star_keyboard)"""
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id, url, reply_text, parse_mode='HTML')
    return ConversationHandler.END
