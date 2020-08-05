from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
cbs = "antricott|chicken_p|chicken_breast|kabbab"
@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def tortia_selection(update, context):

    query = update.callback_query
    data = update.callback_query.data

    user_data = context.user_data

    chat_id = update.effective_message.chat_id

    tortia_selection_keyword = str(data)
    context.user_data['TortiaSelection'] = str(data)
    print("Tortia Selection "+str(tortia_selection_keyword))
    
    user_id = query.from_user.id
    product_keyboard = []
    
    reply_text = emojize(" \U0001F32E לבחירתכם מבחר גדלים להזמנה \U0001F32E \n\n")
#    text_first_button = update.callback_query.message.reply_markup.inline_keyboard[0][0].text

    for size in db.sizes.find({}):

        button_name = emojize(size['SizeName'])
        price = str(size['Price'])
        button_name += emojize(" " + str(price) + " ש\"ח")

        button_callback = size['callback']


        product_keyboard += [[InlineKeyboardButton(button_name, callback_data=button_callback)]]

    
    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")


    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_tortias"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_sizes = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_sizes)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(tortia_selection_keyword))
    return states.FIRST
