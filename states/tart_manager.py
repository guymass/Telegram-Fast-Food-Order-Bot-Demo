from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
from random import choice
from settings import CHATID
cbs = "reg_tortia|med_tortia|large_tortia"

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def tart_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data

    user_data = context.user_data
    user_id = user_data['user_id']
    tortia_selection = context.user_data['TortiaSelection']
    selection_title = ""

    if tortia_selection == "cb_antricott":
        selection_title = "Antricott"
    elif tortia_selection == "cb_chicken_p":
        selection_title = "Chicken Shnitzel"
    elif tortia_selection == "cb_chicken_breast":
        selection_title = "Chicken Breast"
    elif tortia_selection == "cb_kabbab":
        selection_title = "קבב"
    
    #user_id = query.from_user.id
    chat_id = update.effective_message.chat_id

    meal_size_keyword = str(data)

    randomCartId = context.user_data['CartId']
    print("Cart ID" + str(randomCartId)) 
    
    product_keyboard = []
    c_sizes = db.sizes.find({})
  
    for size in c_sizes:
        
        if meal_size_keyword == size['callback']:
            print("SELECTED SIZE" + str(meal_size_keyword))


            reply_text = emojize(" \U0001F32E Your selection {} {} was saved. \U0001F32E \n\n".format(selection_title, size['SizeName']))            

            
            context.user_data['UserTortiaSelection'] = selection_title
            context.user_data['UserTortiaSize'] = size['SizeName']
            context.user_data['UserTortiaPrice'] = size['Price']
            #data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(selection_title) + ' ' +  size['SizeName'], 'Price': size['Price'] }
            #db.cart.insert_one(data)
            
            
            pass

        else: 
            print("MEAL SIZE SELECTION: >>" + str(meal_size_keyword))
            print("CALLBACK:"+str(size['callback']))
            pass
            
#    text_first_button = update.callback_query.message.reply_markup.inline_keyboard[0][0].text


    reply_text += emojize(" \U0001F374 Please select this course salads: ")

    tortia_sald_choice = emojize(" \U0001F957 Salads")
    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U000021AA Cancel")
#    completed_text = emojize(" \U000021AA Finish")

    product_keyboard +=  [[InlineKeyboardButton(tortia_sald_choice, callback_data="cb_tortia_salad")]]
    
    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_tortias"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_cart = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_cart)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(meal_size_keyword))
    return states.FIRST