from telegram.ext import Filters
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (deco, states)
from lib.database import db

#######################################################
# This File is not needed to run the bot but serves as an older example of how I tried to work with Telegra Polls
# If you choose to delete this file make sure to remove it also from the __init__.py file.
#

@deco.run_async
@deco.register_state_message(states.FORTH, Filters.text, pass_user_data=True, pass_chat_data=True, pass_update_queue=True)
def add_notes(update, context):
    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['address'] = text
    category = context.user_data['address']

    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)
    if category != 0:

        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Address": category}
        },upsert=True
        )

        update.message.reply_text("Another way of trying to get notes from user, this file is not needed and is an older version.", reply_markup=reply_markup_cancel)
        return states.FIFTH
