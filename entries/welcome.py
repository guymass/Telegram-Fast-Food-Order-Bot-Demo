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
    reply_text = " \U0001F354 Welcome {}, to begin please press <b>/Start</b>".format(fullname)
    chat_id = update.effective_chat.id
    context.bot.send_photo(chat_id, url, reply_text, parse_mode='HTML')
    return ConversationHandler.END
