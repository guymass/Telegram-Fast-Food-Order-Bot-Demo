from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler,
                          Filters)
from telegram.utils.helpers import mention_html
from emoji import emojize
from lib import (common, deco, states, utils)
from lib.database import db
from random import choice
from settings import CHATID
cbs = "tortia_salad"
keys = ["poll1_tortia_choices", "poll2_tortia_choices"]

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
@deco.register_state_callback("poll1", pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def tortia_salad(update, context):
    global keys 

    query = update.callback_query
    data = update.callback_query.data
    tortia_dish_text = ""
    user_data = context.user_data
    user_id = user_data['user_id']
    tortia_selection = context.user_data['TortiaSelection']
    randomCartId = context.user_data['CartId']
    product_keyboard = []

    selection_title = ""
    if tortia_selection == "cb_antricott":
        selection_title = "Antricott"
    elif tortia_selection == "cb_chicken_p":
        selection_title = "Chicken Stake"
    elif tortia_selection == "cb_chicken_breast":
        selection_title = "Chicken Breast"
    elif tortia_selection == "cb_kabbab":
        selection_title = "Kebbab"
    user_selection_title = context.user_data['UserTortiaSelection']
    user_selection_size = context.user_data['UserTortiaSize']
    user_selection_price = context.user_data['UserTortiaPrice']
    
    tortia_dish_text = user_selection_title + " " + user_selection_size + " "

    questions_all_salads = ["Salad (Cucamber and Tomato)", "Lettuce Salad", "Spicy Onion Salad", "Onion Salad", "Shifka (hot)", "Sweet Salsa", "Spicy Salsa", "Chimichuri", "Lemon", "Turkish Salad", "Tahina", "Avocado Salad"]

    reply_text = emojize("\n Your selection {} was saved.".format(tortia_dish_text))
    salad_manager = emojize(" \U000021AA Approve")
    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U000021AA Cancel")

    payload_key=keys[0]
    poll=utils.multi_selection_widget(
        options=questions_all_salads,
        question=" \U0001F371 Please select your salads for {} course. \n".format(selection_title),
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

def poll2(answer, update, context):
    global keys
    tortia_side_choice = ["Chips", "Onion Rings", "Fried Cabbage", "Potatos"]
    print(context.bot_data["poll1"]["answer"])
    context.user_data['Poll1Answer'] = context.bot_data["poll1"]["answer"]
    cancel_text = emojize(" \U000021AA Cancel")
    back_button = emojize(" \U000021AA Back")
    payload_key=keys[1]
    poll=utils.multi_selection_widget(
        #options=list(f"Option: {i}" for i in range(4)),
        options = tortia_side_choice,
        question=" \U0001F35F Please select only one course! \n",
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
    user_selection_title = context.user_data['UserTortiaSelection']
    user_selection_size = context.user_data['UserTortiaSize']
    user_selection_price = context.user_data['UserTortiaPrice']
    selected_salads = ", ".join(context.user_data[keys[0]]["answer"])
    selected_side = ", ".join(context.user_data[keys[1]]["answer"])
    tortia_dish_text = user_selection_title + " " + user_selection_size + ", With the following selections: \n Salads: {}".format(selected_salads) + "\nSide course: {} ".format(selected_side)
    #text=""
    #text+="\n  Salads: "+str(context.chat_data[keys[0]]["answer"])+"\n"
    #text+=" תוספת: "+str(context.chat_data[keys[1]]["answer"])+"\n"

    data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(tortia_dish_text), 'Price': user_selection_price }
    db.cart.insert_one(data)
    
    reply_text = "Your Order Details: \n"
    reply_text += "\n  "+str(tortia_dish_text)+"\n"

    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U000021AA Cancel")

    completed_text = emojize(" \U000021AA Approve")

    end_poll_keyboard = [[InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_completed")]]
    reply_markup_end_polls = InlineKeyboardMarkup(end_poll_keyboard)
    context.bot.send_message(update.effective_chat.id, tortia_dish_text, reply_markup=reply_markup_end_polls)  
    #query.edit_message_text(reply_text, reply_markup=reply_markup_end_polls)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(tortia_dish_text))
    return states.FIRST