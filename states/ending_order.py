from telegram.ext import Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lib import (deco, states)
from lib.database import db

@deco.run_async
@deco.register_state_message(states.FIFTH, Filters.text, pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def ending_order(update, context):
    user_id = update.effective_message.from_user.id
    #text = ''.join(context.args)
    text = update.message.text
    context.user_data['note'] = text
    category = context.user_data['note']

    print("TYPING >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> " + str(text))

    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("✅ Approve", callback_data="done")], [InlineKeyboardButton("❌ Cancel", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)

    if category != 0:

        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Message": category}
        },upsert=True
        )

        update.message.reply_text(" Thank you for your purchace! You can cancel your order by clicking the cancel buttin at any time.\n", reply_markup=reply_markup_cancel)
    return states.SIXTH
