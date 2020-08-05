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
        selection_title = "ארוחה רגילה"
        context.user_data['UserSelectedMeal'] = selection_title
        print("TORTIA SELECTION: $$$$$$$ " + str(selection_title))
    elif keyword == "cb_double_meal":
        selection_title = "ארוחה כפולה"
        context.user_data['UserSelectedMeal'] = selection_title
        print("TORTIA SELECTION: $$$$$$$ " + str(selection_title))
    elif keyword == "cb_triple_meal":
        selection_title = "ארוחה משולשת"
        context.user_data['UserSelectedMeal'] = selection_title
        print("TORTIA SELECTION: $$$$$$$ " + str(selection_title))
    
    product_keyboard = []
    """c_tortias = db.tortias.find({})
    for s_tort in c_tortias:
        if s_tort['callback'] == keyword:
            #res1 = db.cart.update({'CartId':randomCartId}, {'$set':{'Order':s_tort['ItemName'] }})
            #res2 = db.cart.update({'CartId':randomCartId}, {'$set':{'Price':int(50.00)}})
            #res1 = db.cart.update({"CartId": randomCartId}, {"$set": {"Order": s_tort['ItemName']}})
            #res2 = db.cart.update({"CartId": randomCartId}, {"$set": {"Price": 50.00}})
            if keyword == "cb_regulare_meal":
                #data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(selection_title) + ' ' +  s_tort['ItemName'], 'Price': 50.00 }
                context.user_data['UserSelectedMeal'] = selection_title
                context.user_data['UserMealPrice'] = 50.00

            elif keyword == "cb_double_meal":
                #data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(selection_title) + ' ' +  s_tort['ItemName'], 'Price': 60.00 }
                context.user_data['UserSelectedMeal'] = selection_title
                context.user_data['UserMealPrice'] = 60.00
            elif keyword == "cb_triple_meal":
                #data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(selection_title) + ' ' +  s_tort['ItemName'], 'Price': 75.00 }
                context.user_data['UserSelectedMeal'] = selection_title
                context.user_data['UserMealPrice'] = 75.00
            #db.cart.insert_one(data)
            

            reply_text = emojize("\U0000200F \U0001F32E אנא בחרו את התוספות למנה {}.\U0001F32E \n\n".format(s_tort['ItemName']))
            print("S_TORT_CB " + str(s_tort['callback']) )
            print("ItemName: " + str(s_tort['ItemName']))
        else: 

            pass"""
#    text_first_button = update.callback_query.message.reply_markup.inline_keyboard[0][0].text


    salad_manager = emojize("\U0000200F \U000021AA אישור בחירה")
    back_button = emojize("\U0000200F \U000021AA חזרה")
    cancel_text = emojize("\U0000200F \U00002716 ביטול")
    completed_text = emojize("\U0000200F \U00002611 הזמן עכשיו")


    questions_all_salads = ["סלט ירקות", "סלט חסה", "סלט בצל חריף", "סלט בצל לא חריף", "שיפקה", "סלסה מתוקה", "סלסה חריפה", "צ\'ימיצ\'ורי", "לימון", "סלט טורקי", "טחינה", "אבוקדו"]

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

    product_keyboard +=  [[InlineKeyboardButton(back_button, callback_data="cb_back_tortias"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_cart = InlineKeyboardMarkup(product_keyboard)

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
    user_selected_meal = context.user_data['UserSelectedMeal']
    print("USER SELECTED MEAL: )))))))))))))) " + str(user_selected_meal))
    user_meal_price = context.user_data['UserMealPrice'] 
    selected_salads = ", ".join(context.user_data[keys[0]]["answer"])
    selected_side = ", ".join(context.user_data[keys[1]]["answer"])
    meal_dish_text = user_selected_meal + ", עם התוספות הבאות: \n סלטים: {}".format(selected_salads) + "\nתוספת: {} ".format(selected_side)


    data = {'CartId':randomCartId, 'UserOrderId':user_id, 'Order':str(meal_dish_text), 'Price': user_meal_price }
    db.cart.insert_one(data)
    
    reply_text = "\U0000200F להלן פרטי המנה שהזמנתם: \n"
    reply_text += "\n \U0000200F "+str(meal_dish_text)+"\n"

    back_button = emojize("\U0000200F \U000021AA המשך הזמנה")
    cancel_text = emojize("\U0000200F \U00002716 ביטול")

    completed_text = emojize("\U0000200F \U00002611 אשר הזמנה")

    end_poll_keyboard = [[InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_completed")]]
    reply_markup_end_polls = InlineKeyboardMarkup(end_poll_keyboard)
    context.bot.send_message(update.effective_chat.id, meal_dish_text, reply_markup=reply_markup_end_polls)  
    #query.edit_message_text(reply_text, reply_markup=reply_markup_end_polls)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"+str(meal_dish_text))
    return states.FIRST
