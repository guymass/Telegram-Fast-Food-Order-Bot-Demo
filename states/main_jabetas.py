from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern='^cb_menu_sandwitch|cb_back_jabetas$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def main_jabetas(update, context):

    query = update.callback_query
    data = update.callback_query.data

    user_data = context.user_data

    chat_id = update.effective_message.chat_id

    keyword = str(data)
    print("JABETAS KEYWORD >>>>> "+str(keyword))

    user_id = query.from_user.id
    product_keyboard = []
    reply_text = ""
    
#    text_first_button = update.callback_query.message.reply_markup.inline_keyboard[0][0].text

    for item in db.jabetas.find({}):

        button_name = emojize("\U0000200F \U0001F7E0 " + str(item['ItemName']))
        price = str(item['Price'])
        button_name += emojize(" " + str(price) + " ש\"ח")

        button_callback = item['callback']


        product_keyboard += [[InlineKeyboardButton(button_name, callback_data=button_callback)]]

    
    reply_text = emojize("\U0000200F \U0001F32F לבחירתכם מבחר ג'בטות פריכות, חמות וטעימות \U0001F32F \n\n")
    
    back_button = emojize("\U0000200F \U000021AA חזרה")
    cancel_text = emojize("\U0000200F \U00002716 ביטול")



    #completed_text = emojize("\U0000200F \U00002611 הזמן עכשיו")


    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    
    product_keyboard = list(product_keyboard)
    reply_markup_jabetas = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_jabetas)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(keyword))
    return states.FIRST
