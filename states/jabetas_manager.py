from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

cbs = "jabeta_ant|jabeta_chicken1|jabeta_chicen2|jabeta_s|upgrade_20"
@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def jabetas_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    user_data = context.user_data
    selection_jabetas = str(data)
    print("JABETAS SELECTION: >> " + str(selection_jabetas))

    chat_id = update.effective_message.chat_id

    product_keyboard = []
    jabeta_selection = []
    meal_text = ""

    randomCartId = user_data['CartId']
    print("Cart ID" + str(randomCartId))

    
    jabeta_title = ""
    jab_cursor = db.jabetas.find({})

    for jb in jab_cursor:
        print(jb['callback'])

        if selection_jabetas == jb['callback']:
            meal_text = str(jb['ItemName']) #+ ' ' + str(jb['Price']) + " ש\"ח"
            context.user_data["UserJabetaSelection"] = jb["ItemName"]
            context.user_data["UserJabetaPrice"] = jb["Price"]
            #data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':jb['ItemName'], 'Price': jb['Price']}
            #db.cart.insert_one(data)
        else:
            pass

    reply_text = emojize(" \U0001F32F אנא בחרו את התוספות למנה {}. \U0001F32F \n\n".format(meal_text))
    jabeta_sald_choice = emojize(" \U0001F957 Salad Choice")
    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")
    #completed_text = emojize(" \U00002611 הזמן עכשיו")
    product_keyboard +=  [[InlineKeyboardButton(jabeta_sald_choice, callback_data="cb_jabeta_salad")]]
    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_jabetas"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_jabetas_selected = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_jabetas_selected)
    print("JJJJJJJJJJJJJJJJJJJJJ " + str(meal_text))
    return states.FIRST
