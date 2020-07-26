from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

cbs = "water|soda|cola|fanta|sprite|eshcolit|nana|orange|grapes|apple|icetee"
@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def jabetas_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    user_data = context.user_data
    selection_drinks = str(data)
    print("DRINK SELECTION: >> " + str(selection_drinks))

    chat_id = update.effective_message.chat_id

    product_keyboard = []
    extra_selection = []
    meal_text = ""

    randomCartId = user_data['CartId']
    print("Cart ID" + str(randomCartId))

    
    drinks_title = ""
    d_cursor = db.drinks.find({})

    for dr in d_cursor:
        print(dr['callback'])

        if selection_drinks == dr['callback']:
            meal_text = str(dr['ItemName']) + '  $' + str(dr['Price']) 
            data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':dr['ItemName'], 'Price': dr['Price']}
            db.cart.insert_one(data)
        else:
            pass

    reply_text = emojize(" \U0001F964 Your choice {} was saved! Please continue shopping or hit the Finish buttong to complete the order.\U0001F964 \n\n".format(meal_text))

    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U000021AA Cancel")
    completed_text = emojize(" \U000021AA Finish")

    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_drinks"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_completed")]]
    product_keyboard = list(product_keyboard)
    reply_markup_drink_selected = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_drink_selected)
    print("XXXXXXXXXXXXXXXX" + str(meal_text))
    return states.FIRST
