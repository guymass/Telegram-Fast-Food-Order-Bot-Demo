from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states, utils)
from lib.database import db
from random import choice
from settings import CHATID
cbs = "regulare_meal|double_meal|triple_meal"
keys = ["poll1_meal_choices", "poll2_meal_choices"]

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
@deco.register_state_callback("poll1", pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def meal_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data

    user_data = context.user_data
    user_id = user_data['user_id']
    randomCartId = context.user_data['CartId']
    tortia_selection = context.user_data['TortiaSelection']
    chat_id = update.effective_message.chat_id
    keyword = str(data)

    selection_title = ""

    if keyword == "cb_regulare_meal":
        selection_title = "Regulare Meal"
        context.user_data['UserSelectedMeal'] = selection_title
        context.user_data['UserMealPrice'] = 50.00
        print("TORTIA SELECTION: $$$$$$$ " + str(selection_title))
    elif keyword == "cb_double_meal":
        selection_title = "Double Meal"
        context.user_data['UserSelectedMeal'] = selection_title
        context.user_data['UserMealPrice'] = 60.00
        print("TORTIA SELECTION: $$$$$$$ " + str(selection_title))
    elif keyword == "cb_triple_meal":
        selection_title = "Triple Meal"
        context.user_data['UserSelectedMeal'] = selection_title
        context.user_data['UserMealPrice'] = 75.00
        print("TORTIA SELECTION: $$$$$$$ " + str(selection_title))
    
    product_keyboard = []

    salad_manager = emojize(" \U000021AA Approve")
    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")
    completed_text = emojize(" \U00002611 הזמן עכשיו")


    questions_all_salads = ["Vegetable Salad", "Lettuce Salad", "Spicy Onion Salad", "Onion Salad", "Spicy Shifka", "Sweet Salsa", "Spicy Salsa", "Chimichuri", "Lemon", "Turkish Salad", "Tahina", "Avocado"]
    
    payload_key=keys[0]
    poll=utils.multi_selection_widget(
        options=questions_all_salads,
        question=" \U0001F371 Please choose the salads for {}. \n".format(selection_title),
        n_columns=2,
        spacing=5,        
        checked_symbol="✅", 
        unchecked_symbol="☑️",
        cancel_buttons=[
            InlineKeyboardButton(cancel_text, callback_data="cancel"),
        #    InlineKeyboardButton(back_button, callback_data="back_1")
        ],
        payload_key=payload_key,
#        callback_data="tortia_poll_2"
        callback=poll2
    )

    poll.send(update, context)

    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_tortias"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_cart = InlineKeyboardMarkup(product_keyboard)

def poll2(answer, update, context):
    global keys
    tortia_side_choice = ["Fried Chips", "Onion Rings", "Fried Cabbage", "Potatos"]
    #print(context.bot_data["poll1"]["answer"])
#    context.user_data['Poll1Answer'] = context.bot_data["poll1"]["answer"]
    cancel_text = emojize(" \U00002716 Cancel")
    back_button = emojize(" \U000021AA Back")
    payload_key=keys[1]
    poll=utils.multi_selection_widget(
        #options=list(f"Option: {i}" for i in range(4)),
        options = tortia_side_choice,
        question=" \U0001F35F PLease select only one choice! \n",
        single_option=True,
        n_columns=1,
        spacing=5,
        checked_symbol="✅", 
        unchecked_symbol="☑️",
        payload_key=payload_key,
        confirm_button_text="Approve",
        cancel_buttons=[
            InlineKeyboardButton(cancel_text, callback_data="cancel"),
            InlineKeyboardButton(back_button, callback_data="poll1")
        ],
        callback=finish
    )

    poll.send(update, context)


def finish(choices, update, context):    
    global keys
    user_data = context.user_data
    user_id = user_data['user_id']
    randomCartId = context.user_data['CartId']
    user_selected_meal = context.user_data['UserSelectedMeal']
    print("USER SELECTED MEAL: )))))))))))))) " + str(user_selected_meal))
    user_meal_price = context.user_data['UserMealPrice'] 
    selected_salads = ", ".join(context.user_data[keys[0]]["answer"])
    selected_side = ", ".join(context.user_data[keys[1]]["answer"])
    meal_dish_text = user_selected_meal + ", With the following salads: \n {}".format(selected_salads) + "\nWith extra course, {} ".format(selected_side)


    data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(meal_dish_text), 'Price': user_meal_price }
    db.cart.insert_one(data)
    
    reply_text = "You Order Details: \n"
    reply_text += "\n  "+str(meal_dish_text)+"\n"
    reply_text += "Would you like to add a drink?"
    drinks_button = emojize(" \U0001F964 Cold Drinks")
    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")

    completed_text = emojize(" \U00002611 Approve")

    end_poll_keyboard = [[InlineKeyboardButton(drinks_button, callback_data="cb_menu_drinks"), InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_completed")]]
    reply_markup_end_polls = InlineKeyboardMarkup(end_poll_keyboard)
    context.bot.send_message(update.effective_chat.id, meal_dish_text, reply_markup=reply_markup_end_polls)  
    #query.edit_message_text(reply_text, reply_markup=reply_markup_end_polls)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(meal_dish_text))
    return states.FIRST
