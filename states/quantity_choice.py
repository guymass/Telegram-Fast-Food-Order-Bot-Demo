from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from lib import (deco, states)
from lib.database import db


#######################################################
# This File is not needed to run the bot but serves as an older example of how I tried to work with Telegra Polls
# If you choose to delete this file make sure to remove it also from the __init__.py file.
#

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern='^qty[1-6]$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def quantity_choice(update, context):
    #chat_id = update.effective_message.chat_id
    query = update.callback_query
    data = update.callback_query.data
    message = query.message
    user_data = context.user_data
    user_id = query.from_user.id

    keyword = str(data)
    if keyword == "qty1":
        context.user_data['quantity'] = "5"
        category = context.user_data['quantity']


        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Quantity": category}
        },upsert=True
        )

        query.edit_message_text(" 👩‍🌾 מצויין! בחרתם: {} \n".format(category))
        pass

    elif keyword == "qty2":
        context.user_data['quantity'] = "10"
        category = context.user_data['quantity']


        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Quantity": category}
        },upsert=True
        )

        query.edit_message_text(" 👩‍🌾 מצויין! בחרתם: {} \n".format(category))
        pass

    elif keyword == "qty3":
        context.user_data['quantity'] = "15"
        category = context.user_data['quantity']


        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Quantity": category}
        },upsert=True
        )

        query.edit_message_text(" 👩‍🌾 מצויין! בחרתם: {} \n".format(category))
        pass

    elif keyword == "qty4":
        context.user_data['quantity'] = "20"
        category = context.user_data['quantity']


        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Quantity": category}
        },upsert=True
        )

        query.edit_message_text(" 👩‍🌾 מצויין! בחרתם: {} \n".format(category))
        pass

    elif keyword == "qty5":
        context.user_data['quantity'] = "25"
        category = context.user_data['quantity']


        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Quantity": category}
        },upsert=True
        )

        query.edit_message_text(" 👩‍🌾 מצויין! בחרתם: {} \n".format(category))
        pass

    elif keyword == "qty6":
        context.user_data['quantity'] = "30"
        category = context.user_data['quantity']


        doc = db.tmp_orders.find_one_and_update(
        {"UserId": user_id},
        {"$set":
            {"Quantity": category}
        },upsert=True
        )

        query.edit_message_text(" 👩‍🌾 מצויין! בחרתם: {} \n".format(category))
        pass


    chat_id=query.message.chat_id,

    cancel_keyboard = []
    cancel_keyboard =  [[InlineKeyboardButton("ביטול", callback_data="cancel")]]
    cancel_keyboard = list(cancel_keyboard)
    reply_markup_cancel = InlineKeyboardMarkup(cancel_keyboard)

    query.edit_message_text(text=" 👩‍🌾 מצויין! בחרתם {} \n\n 💬 אנא רשמו ושלחו לי את שמכם המלא, אני ממתין...⏳".format(category), reply_markup=reply_markup_cancel)

    return states.SECOND