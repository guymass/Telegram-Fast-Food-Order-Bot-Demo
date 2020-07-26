from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

cbs = "hum_300|hum_220|hum_150|hum_extra"
@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def hum_selection(update, context):

    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    product_keyboard = []
    user_data = context.user_data
    reply_text= ""
    chat_id = update.effective_message.chat_id
   
    hum_selection_keyword = str(data)
    context.user_data['HumMakeSelection'] = hum_selection_keyword
    
    print("Humburger Selection "+str(hum_selection_keyword))
    hum_list = ['cb_hum_300', 'cb_hum_220', 'cb_hum_150']
    cursor_cart = db.cart.find({})
    cart_id = ""
    for cart in cursor_cart:
        
        if user_id == cart['UserOrderId']:
            cart_id = cart['CartId'] 
            print("CART ID IS: " + str(cart_id))
        else:
            print("No Such Cart ID Found!!! ")
            
        if cart_id != "" and cart_id == context.user_data['CartId'] :
            
            print("Cart IDs Match:##")
        else:
            print("Cart ID is empty or a missmatch!")
    
        if data in hum_list:
            context.user_data['HumTitle'] = cart['Order']

        if hum_selection_keyword == "cb_hum_extra":
            context.user_data['HumburgerExtra'] = hum_selection_keyword
             
            reply_text = emojize(" \U0001F354 Size Me Up selection was saved. \U0001F354 \n\n")
            meal_text = "Size Me Up {} for $10".format(cart['Order'])
            #data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(meal_text), 'Price':sel['Price']  }
            #doc = db.cart.find_one_and_update({"CartId": cart_id, 'UserOrderId':user_id,}, {"$set": {"Order": meal_text}}, upsert=True)
            #doc2 = db.cart.find_one_and_update({"CartId": cart_id, 'UserOrderId':user_id,}, {'$inc':{"Price":10 }}, upsert=True)
            #data = {'CartId':cart_id, 'UserOrderId':user_id, 'Order':str(meal_text), 'Price': 10}
            #db.cart.insert_one(data)
        else:
            pass
    
    if hum_selection_keyword in hum_list :
        context.user_data['HumburgerSelection'] = hum_selection_keyword
        reply_text = emojize(" \U0001F354 Please select how you want your course made: \U0001F354 \n\n")

        medium_button = emojize(" \U0001F969 Medium")
        well_button = emojize(" \U0001F969 Well")
        welldone_button = emojize(" \U0001F969 Well Done")
        product_keyboard +=  [[InlineKeyboardButton(medium_button, callback_data="cb_medium_humburger"), InlineKeyboardButton(well_button, callback_data="cb_well_humburger"), InlineKeyboardButton(welldone_button, callback_data="cb_welldone_humburger")]]


    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U000021AA Cancel")

    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_humburgers"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_sizes = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_sizes)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(hum_selection_keyword))
    return states.FIRST
