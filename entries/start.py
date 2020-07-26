from emoji import emojize
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)
from lib import (common, deco, states)
from lib.database import db
import logging
from random import choice
from settings import CHATID

logger = logging.getLogger(__name__)

@deco.run_async
@deco.conversation_command_handler("start", pass_args=True)
def start(update, context):
    keys = ["poll1_choices", "poll2_choices"]
    for k in keys:
        context.chat_data[k]={}

    result = db.images.find_one_and_delete({"ImageText": "logo"})
    query = update.callback_query

    chat_id = update.effective_chat.id
    user_id = update.message.from_user.id
    username = update.message.from_user.username
    message_date = update.message.date
    message_id = update.message.message_id
    first_name = update.effective_message.from_user.first_name
    last_name = update.effective_message.from_user.last_name

    fullname = str(first_name) #+ " " + str(last_name)

    text = update.message.text

    item = {
        "MessageId":message_id,
        "MessageText":text
    }

    if db.messages.count_documents({'MessageId': message_id}, limit=1) > 0:
        print("הודעה רשומה כבר!" + str(message_id))
        pass
    else:
        db.messages.insert_one(item)
        print("ההודעה נשמרה ;-)" + str(message_id))

# Create use cart to save selections and delete if one already exists for user.

    if db.cart.count_documents({'UserOrderId': user_id}, limit=1) > 0:
        result = db.cart.find_one_and_delete({'UserOrderId': user_id})
    else:
        randomCartId = common.randStr(N=10)
        context.user_data['CartId'] = str(randomCartId)
    
    
    randomCartId = common.randStr(N=10)
    context.user_data['CartId'] = str(randomCartId)
    res = db.logo.find_one({"ImageText":"logo"})
    url = res['ImageId']
    msg = " \U0001F3AF \U0001F3AF \U0001F3AF \U0001F3AF \U0001F3AF \U0001F3AF \U0001F3AF \U0001F3AF \U0001F3AF \U0001F3AF \n\n"
    msg += " \U0001F4CB Welcome {} \n This is our demo orders bot for you to tryout.\n".format(fullname)+"\n\n"
    message = emojize(str(msg))
    user_full_details = emojize(str(user_id) + " - " + str(username))
    context.bot.send_photo(chat_id, url, message, parse_mode='HTML')
    #context.bot.send_message(-1001221668754, user_full_details, parse_mode="HTML")
    user = update.effective_message.from_user

    logger.info("User %s started the conversation.", user.first_name)
    user_id = update.effective_message.from_user.id
    username = update.effective_message.from_user.username
    message_date = update.effective_message.date
    msg_id = update.effective_message.message_id

    fullname = str(user.first_name) #+ " " +str(user.last_name)

    print(username)
    print(fullname)
    print(user_id)
    print(chat_id)
    print(msg_id)

    context.user_data['user_id'] = user_id
    context.user_data['fullname'] = fullname
    context.user_data['username'] = username
    context.user_data['start_message_id'] = msg_id
    #context.user_data['location'] = location
    details = context.user_data
    user_Mobile = ""
    user_location = ""
    reply_keyboard = []
    items = []

    order = {
            "UserId":user_id,
            "UserName": str(username),
            "FullName":str(fullname),
            "ProductText": "", #from button selection
            "Quantity":"", #from button selection
            "Mobile":"", #from button selection
            "Address":"", #from contact location optional!
            "Message":"",
            "Status":"Pending", # Dispatched/Delivered
            "Date":message_date
        }
    db.tmp_orders.insert_one(order)

    reply_text = ""

    if context.user_data != "":
        reply_text += "\U0001F468 Welcome back {}\n".format(fullname)

    else:
        reply_text += "\n To start your order {} please click the start button".format(fullname) + "\nYou can add as many items as you require untill you choose to end the order. You may cancel at anytime and start a new order in case you made a mistake.\n"


    begin_text = emojize(" \U00002611 Start Order ")
    cancel_text = emojize("\U00002716 Cancel ")
    begin_text = str(begin_text)
    cancel_text = str(cancel_text)

    start_keyboard = [
            [InlineKeyboardButton(begin_text, callback_data="begin")], [InlineKeyboardButton(cancel_text, callback_data=str("cancel"))]
             ]
    reply_markup_start = InlineKeyboardMarkup(start_keyboard)
    context.bot.send_message(chat_id,
    reply_text,
    reply_markup=reply_markup_start)

    return states.FIRST
