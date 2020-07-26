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
    fullname = context.user_data['fullname']
    opts = []
    o = []
    product_keyboard = []

    if context.user_data.get(text):
        reply_text = ' {} I already have your user details\n' \
                     'The information I have is: \n {}'.format(common.facts_to_str(context.user_data))
    else:
        reply_text = emojize(' \U00002668 \U00002668 Please select the items to add to your order\n\n')
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
            
            elif item['ButtonName'] == "Jabeta Sandwitch":
                button_name = emojize("\U0001F32F " + str(item['ButtonName']))
                button_callback = item['callback']

            elif item['ButtonName'] == "Extras":
                button_name = emojize("\U0001F35F " + str(item['ButtonName']))
                button_callback = item['callback']

            elif item['ButtonName'] == "Cold Drinks":
                button_name = emojize("\U0001F964 " + str(item['ButtonName']))
                button_callback = item['callback']
            else:
                pass

            product_keyboard += [[InlineKeyboardButton(button_name, callback_data=button_callback)]]

        cancel_text = emojize(" \U00002716 Cancel")

        product_keyboard +=  [[InlineKeyboardButton(cancel_text, callback_data="cancel")]]
        product_keyboard = list(product_keyboard)
        reply_markup_product = InlineKeyboardMarkup(product_keyboard)

        context.bot.send_message(chat_id, text=reply_text, reply_markup=reply_markup_product, parse_mode='HTML')
    
    return states.FIRST

