from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (common, deco, states)
from lib.database import db
from emoji import emojize
from time import sleep

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern='^begin|cb_back$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def start_order(update, context):
    query = update.callback_query
    query.answer()
    text = query
    context.user_data["user_cart"]={}
    user_id = context.user_data['user_id']
    CartId = context.user_data['CartId']
    cursor_cart = db.cart.find({})
    for cur in cursor_cart:
        if cur['UserOrderId'] == str(user_id):
            del_cart = db.cart.delete_many({'UserOrderId': str(user_id)})
        if cur['CartId'] == str(CartId):
            del_cart = db.cart.delete_many({'CartId': str(CartId)})

    fullname = context.user_data['fullname']
    context.user_data["UserPhone"] = ""
    context.user_data["UserAddress"] = ""
    context.user_data["UserComment"] = ""
    context.user_data["UserLocation"] = ""

    opts = []
    o = []
    product_keyboard = []

    if context.user_data.get(text):
        reply_text = 'Your selection is saved! ' \
                     'What I know is: \n {}'.format(common.facts_to_str(context.user_data))
    else:
        reply_text = emojize(' \U00002668 Please select form the menus your choices and when you are ready hit the Approve button to complete your order. \U00002668 \n\n')
        chat_id = update.effective_chat.id

        button_name = ""
        button_callback = ""

        for item in db.mainmenu.find({}):

            if item['ButtonName'] == "Tortias":
                button_name = emojize("\U0001F32E " + str(item['ButtonName']))
                button_callback = item['callback']

            elif item['ButtonName'] == "Hamburgers":
                button_name = emojize("\U0001F354 " + str(item['ButtonName']))
                button_callback = item['callback']
            
            elif item['ButtonName'] == "Jabeta Sandwich":
                button_name = emojize("\U0001F32F " + str(item['ButtonName']))
                button_callback = item['callback']

            elif item['ButtonName'] == "Side Courses":
                button_name = emojize("\U0001F35F " + str(item['ButtonName']))
                button_callback = item['callback']

            elif item['ButtonName'] == "Cold Drinks":
                button_name = emojize("\U0001F964 " + str(item['ButtonName']))
                button_callback = item['callback']
            else:
                pass

            product_keyboard += [[InlineKeyboardButton(button_name, callback_data=button_callback)]]

        my_orders = emojize(" \U00002716 My Orders")
        cancel_text = emojize(" \U00002716 Cancel")
        product_keyboard +=  [[InlineKeyboardButton(my_orders, callback_data="cb_myorders")]]
        product_keyboard +=  [[InlineKeyboardButton(cancel_text, callback_data="cancel")]]
        product_keyboard = list(product_keyboard)
        reply_markup_product = InlineKeyboardMarkup(product_keyboard)

        context.bot.send_message(chat_id, text=reply_text, reply_markup=reply_markup_product, parse_mode='HTML')
    
    return states.FIRST

