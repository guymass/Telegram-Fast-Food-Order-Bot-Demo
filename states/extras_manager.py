from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

cbs = "chips|onion_rings|potatos|cruvit|rice"
@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def jabetas_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    user_data = context.user_data
    selection_extras = str(data)
    print("EXTRAS SELECTION: >> " + str(selection_extras))

    chat_id = update.effective_message.chat_id

    product_keyboard = []
    extra_selection = []
    meal_text = ""

    randomCartId = user_data['CartId']
    print("Cart ID" + str(randomCartId))

    
    extra_title = ""
    ext_cursor = db.extras.find({})

    for ex in ext_cursor:
        print(ex['callback'])

        if selection_extras == ex['callback']:
            meal_text = str(ex['ItemName']) + ' $' + str(ex['Price'])
            data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':ex['ItemName'], 'Price': ex['Price']}
            db.cart.insert_one(data)
        else:
            pass

    reply_text = emojize(" \U0001F32F Your selection {} was saves. Please continue shopping or click the  Finish button to complete the order.\U0001F32F \n\n".format(meal_text))

    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U000021AA Cancel")
    completed_text = emojize(" \U000021AA Finish")

    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_extras"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_completed")]]
    product_keyboard = list(product_keyboard)
    reply_markup_extra_selected = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_extra_selected)
    print("XXXXXXXXXXXXXXXX" + str(meal_text))
    return states.FIRST
