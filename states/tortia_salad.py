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
        selection_title = "אנטריקוט"
    elif tortia_selection == "cb_chicken_p":
        selection_title = "פרגית"
    elif tortia_selection == "cb_chicken_breast":
        selection_title = "חזה עוף"
    elif tortia_selection == "cb_kabbab":
        selection_title = "קבב"
    user_selection_title = context.user_data['UserTortiaSelection']
    user_selection_size = context.user_data['UserTortiaSize']
    user_selection_price = context.user_data['UserTortiaPrice']
    
    tortia_dish_text = user_selection_title + " " + user_selection_size + " "

    questions_all_salads = ["סלט ירקות", "סלט חסה", "סלט בצל חריף", "סלט בצל לא חריף", "שיפקה", "סלסה מתוקה", "סלסה חריפה", "צ\'ימיצ\'ורי", "לימון", "סלט טורקי", "טחינה", "אבוקדו"]

    reply_text = emojize("\n \U0000200F בחירתכם {} התקבלה.".format(tortia_dish_text))
    salad_manager = emojize("\U0000200F \U000021AA אישור בחירה")
    back_button = emojize("\U0000200F \U000021AA חזרה")
    cancel_text = emojize("\U0000200F \U00002716 ביטול")

    payload_key=keys[0]
    poll=utils.multi_selection_widget(
        options=questions_all_salads,
        question="\U0000200F \U0001F371  אנא בחרו את הסלטים למנה {} \n".format(selection_title),
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
    tortia_side_choice = ["צ'יפס", "טבעות בצל", "כרובית", "פוטטוס"]
    print(context.bot_data["poll1"]["answer"])
    context.user_data['Poll1Answer'] = context.bot_data["poll1"]["answer"]
    cancel_text = emojize("\U0000200F \U00002716 ביטול")
    back_button = emojize("\U0000200F \U000021AA חזרה")
    payload_key=keys[1]
    poll=utils.multi_selection_widget(
        #options=list(f"Option: {i}" for i in range(4)),
        options = tortia_side_choice,
        question="\U0000200F \U0001F35F אנא בחרו תוספת אחת!  \n",
        single_option=True,
        n_columns=1,
        spacing=5,
        checked_symbol="✅", 
        unchecked_symbol="☑️",
        payload_key=payload_key,
        confirm_button_text="אישור",
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
    tortia_dish_text = user_selection_title + " " + user_selection_size + ", עם התוספות הבאות: \n סלטים: {}".format(selected_salads) + "\nתוספת: {} ".format(selected_side)
    #text=""
    #text+="\n \U0000200F סלטים: "+str(context.chat_data[keys[0]]["answer"])+"\n"
    #text+="\U0000200F תוספת: "+str(context.chat_data[keys[1]]["answer"])+"\n"

    data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(tortia_dish_text), 'Price': user_selection_price }
    db.cart.insert_one(data)
    
    reply_text = "\U0000200F להלן פרטי המנה שהזמנתם: \n"
    reply_text += "\n \U0000200F "+str(tortia_dish_text)+"\n"
    reply_text += "להוספת שתיה בחרו מתפריט המשקאות."
    drinks_button = emojize("\U0000200F \U0001F964 שתיה קרה")
    back_button = emojize("\U0000200F \U000021AA לתפריט הקודם")
    cancel_text = emojize("\U0000200F \U00002716 ביטול")

    completed_text = emojize("\U0000200F \U00002611 אשר הזמנה")

    end_poll_keyboard = [[InlineKeyboardButton(drinks_button, callback_data="cb_menu_drinks"), InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_completed")]]
    reply_markup_end_polls = InlineKeyboardMarkup(end_poll_keyboard)
    context.bot.send_message(update.effective_chat.id, tortia_dish_text, reply_markup=reply_markup_end_polls)  
    #query.edit_message_text(reply_text, reply_markup=reply_markup_end_polls)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(tortia_dish_text))
    return states.FIRST