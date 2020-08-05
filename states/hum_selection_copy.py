from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

cbs = "hum_300|hum_220|hum_150|hum_extra"
@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def hum_selection_copy(update, context):

    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    product_keyboard = []
    user_data = context.user_data
    reply_text= ""
    chat_id = update.effective_message.chat_id

    hum_selection_keyword = str(data)
    context.user_data['HumMakeSelection'] = hum_selection_keyword
    cart_id = context.user_data['CartId']
    print("Humburger Selection "+str(hum_selection_keyword))
    hum_list = ['cb_hum_300', 'cb_hum_220', 'cb_hum_150']
    cursor_cart = db.cart.find({})

    for cart in cursor_cart:
        if cart['CartId'] == cart_id:

            if hum_selection_keyword == "cb_hum_extra":
                context.user_data['HumburgerExtra'] = hum_selection_keyword
                reply_text = emojize(" \U0001F354 Topup for 5$ was added! \U0001F354 \n\n")
                meal_text = "Topup for 5$"
                #data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(meal_text), 'Price':sel['Price']  }
                doc = db.cart.find_one_and_update({"CartId": cart_id, 'UserOrderId':user_id,}, {"$set": {"HumburgerExtra": meal_text}}, upsert=True)
                doc2 = db.cart.find_one_and_update({"CartId": cart_id, 'UserOrderId':user_id,}, {'$inc':{"Price":10, "metrics.orders": 1 }}, upsert=True)
                
    
            elif hum_selection_keyword in hum_list :
                context.user_data['HumburgerSelection'] = hum_selection_keyword
                reply_text = emojize(" \U0001F354 Please select how you want your hamburger made. \U0001F354 \n\n")
        else:
            pass
#    text_first_button = update.callback_query.message.reply_markup.inline_keyboard[0][0].text


    medium_button = emojize(" \U0001F969 Medium")
    well_button = emojize(" \U0001F969 Done")
    welldone_button = emojize(" \U0001F969 Well Done")
    product_keyboard +=  [[InlineKeyboardButton(medium_button, callback_data="cb_medium_humburger"), InlineKeyboardButton(well_button, callback_data="cb_well_humburger"), InlineKeyboardButton(welldone_button, callback_data="cb_welldone_humburger")]]


    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")

    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_humburgers"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_sizes = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_sizes)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(hum_selection_keyword))
    return states.FIRST
