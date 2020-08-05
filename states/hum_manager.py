from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db

cbs = "medium_humburger|well_humburger|welldone_humburger"
@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def hum_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    user_data = context.user_data

    chat_id = update.effective_message.chat_id
    product_keyboard = []
    hum_selection = []
    meal_text = ""
    hum_selection_keyword =  context.user_data['HumburgerSelection']
    hum_make_selection = context.user_data['HumMakeSelection']
    """if context.user_data['HumburgerExtra'] != 0:
        hum_extra_keyword =  context.user_data['HumburgerExtra']
    else:
        pass"""
    print("Humburger Selected: @@ " + str(hum_selection_keyword))
    hum_make_keyword = str(data)
    print("HUM MAKE KEY >> " + str(hum_make_keyword))
    randomCartId = context.user_data['CartId']
    print("Cart ID" + str(randomCartId))

    selection_title = str(hum_selection_keyword)
    make_title = ""

    if hum_make_keyword == "cb_medium_humburger":
        make_title = "Medium"
    elif hum_make_keyword == "cb_well_humburger":
        make_title = "Medium Well"
    elif hum_make_keyword == "cb_welldone_humburger":
        make_title = "Well Done"


    hum_list = ['cb_medium_humburger', 'cb_well_humburger', 'cb_welldone_humburger']
    hum_titles = ['cb_hum_150', 'cb_hum_220', 'cb_hum_300']
    reply_text = ""
    selected_humburger_title = ""
    c_humburgers = db.humburger.find({})
    
    for sel in c_humburgers:
        if hum_selection_keyword in hum_titles and hum_selection_keyword == sel['callback']:
            selected_humburger_title = sel['ItemName']
            print("HUmburger Title >>" + str(selected_humburger_title))
    
        print(sel['callback'])
        if hum_make_keyword != 0 and hum_selection_keyword == sel['callback']:

            meal_text = ""
            

            if hum_make_selection == "cb_hum_extra":
                meal_text += str(selected_humburger_title) + ' -> ' + str(make_title)
                meal_text += " SizeMeUp for 5$ \n"
                price = int(sel['Price'] + 5 )
                context.user_data['UserSelectedHamburger'] = meal_text
                context.user_data['UserHamburgerPrice'] = price
                print("Extra Meal >> : " + str(meal_text))

            elif sel['callback'] in hum_titles:
                meal_text += sel['ItemName'] + ' ' + str(make_title)
                context.user_data['UserSelectedHamburger'] = meal_text
                context.user_data['UserHamburgerPrice'] = sel['Price']
                print("Humburger Meal >> : " + str(meal_text))


        else: 

            pass
    reply_text += emojize(" \U0001F354 Please Choose the salads for {}. \U0001F354 \n\n".format(meal_text))

    hamburger_sald_choice = emojize(" \U0001F957 Salad Choice")
    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")

    product_keyboard +=  [[InlineKeyboardButton(hamburger_sald_choice, callback_data="cb_hamburger_salad")]]
    

    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_humburgers_make"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_hum_manager = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_hum_manager)
    
    return states.FIRST
