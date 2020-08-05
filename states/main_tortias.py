from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern='^cb_menu_tortias|cb_back_tortias$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def main_tortias(update, context):

    query = update.callback_query
    data = update.callback_query.data

    user_data = context.user_data

    chat_id = update.effective_message.chat_id

    keyword = str(data)
    print("KEYWORD >>>>> "+str(keyword))

    user_id = query.from_user.id
    product_keyboard = []
    
    reply_text = emojize(" \U0001F32E לבחירתכם מבחר טורטיות טעימות \U0001F32E \n\n")
#    text_first_button = update.callback_query.message.reply_markup.inline_keyboard[0][0].text

    for item in db.tortias.find({}):

        button_name = emojize(" \U0001F7E1 " + str(item['ItemName']))
        button_callback = item['callback']


        product_keyboard += [[InlineKeyboardButton(button_name, callback_data=button_callback)]]


    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")


    completed_text = emojize(" \U00002611 הזמן עכשיו")


    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_completed")]]
    
    product_keyboard = list(product_keyboard)
    reply_markup_tortias = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_tortias)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(keyword))
    return states.FIRST
