from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Filters
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
from lib.utils import buttons_menu
from random import choice
from settings import CHATID
cbs = "completed"

@deco.run_async
@deco.register_state_callback("location_button", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def location_button(update, context):
    context.user_data["run_next"]=request_user_info
    location_button = KeyboardButton(text="location", request_location=True)
    cancel_button = KeyboardButton(text="Cancel")
    custom_keyboard = [[ location_button, cancel_button]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard,  one_time_keyboard=True,  resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                     text="Please share your location with us for faster delivery. Make sure you have GPS enabled.\n", 
                     reply_markup=reply_markup)

@deco.run_async
@deco.register_state_callback("phone_button", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def phone_button(update, context):
    context.user_data["run_next"]=request_user_info
    contact_button = KeyboardButton(text="Telephone", request_contact=True)
    cancel_button = KeyboardButton(text="Cancel")
    custom_keyboard = [[ contact_button, cancel_button ]]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard,  one_time_keyboard=True,  resize_keyboard=True)
    context.bot.send_message(chat_id=update.effective_chat.id, 
                     text="Please share your telephone with us so we can contact you directly.\n", 
                     reply_markup=reply_markup)

@deco.run_async
@deco.conversation_message_handler(Filters.location,  pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def location_handler(update, context):
    print("Retrieving Location ")
    location = update.effective_message.location
    lat = location.latitude
    lon = location.longitude
    if lat == "" and lon == "":
        context.user_data["UserLocation"] = "Not Shared"
    else:
        context.user_data["UserLocation"] = str(lat) + ", " + str(lon)
    print("Your coordinates: ", lat,lon)
    context.user_data["final_menu"].pop('location_button')
    request_user_info(update, context)

@deco.run_async
@deco.conversation_message_handler(Filters.contact,  pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def phone_handler(update, context):
    context.user_data["run_next"]=None
    print("Retrieving Phone Number ")
    contact = update.effective_message.contact
    phone = contact.phone_number
    if phone == "":
        context.user_data["UserPhone"] = "Not Shared"
    else:
        context.user_data["UserPhone"] = phone
    print("Your phone is: ", phone)
    context.user_data["final_menu"].pop('phone_button')
    request_user_info(update, context)

@deco.run_async
@deco.register_state_callback("add_comment", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def add_comment(update, context):
    context.user_data["run_next"]=handle_add_comment
    context.bot.send_message(chat_id=update.effective_chat.id, 
                     text="Please type your address and send me.\n")

def handle_add_comment(update, context):
    context.user_data["run_next"]=None 
    if update.message.text:
        context.user_data["final_menu"].pop('add_comment')
        print("The sent comment text is: ", update.message.text)
        context.user_data["UserComment"] = update.message.text

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                     text="Please add your notes here in a single text message and send me.")
    request_user_info(update, context)

@deco.run_async
@deco.register_state_callback("write_address", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def write_address(update, context):
    context.user_data["run_next"]=handle_write_address
    context.bot.send_message(chat_id=update.effective_chat.id, 
                     text="Please send me your address")

def handle_write_address(update, context):
    context.user_data["run_next"]=None 
    if update.message.text:
        context.user_data["final_menu"].pop('write_address')
        print("Address received: ", update.message.text)
        context.user_data["UserAddress"] = update.message.text

    else:
        context.bot.send_message(chat_id=update.effective_chat.id, 
                     text="Only use text messages!")
    request_user_info(update, context)



menu_dict={
            # state string : text
            "add_comment": " \U0001F4AC Add a Note",
            "write_address": " \U0001F697 Send Address",
            "location_button": " \U0001F4E1 Share Location",
            "phone_button": " \U0000260E Share Contact",
            "approve": " \U00002705 Approve",
            "cancel": " \U0000274C Cancel",
        }


@deco.run_async
@deco.conversation_command_handler("final", pass_args=True)
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def finalize_operation(update, context):
    print("Cleaning up final menu")
    context.user_data["final_menu"]=False
    print(context.user_data["final_menu"])
    request_user_info(update, context)


def request_user_info(update, context):    
    if not context.user_data.get("final_menu"):
        context.user_data["final_menu"]=menu_dict
        print(context.user_data["final_menu"])
    final_menu=buttons_menu(
        context.user_data["final_menu"],
        question="You can share your contact, address and telephone details and also add location. These are optional, you can click the approve to complete your order and we will contact you though Telegram private chat.",
        n_columns=1
    )
    final_menu.send(update, context)



@deco.run_async
@deco.register_state_callback("approve", pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def complete_order(update, context):
    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    user_data = context.user_data
    user_phone = ""
    user_address = ""
    user_location = ""
    user_comment = ""

    randomCartId = user_data['CartId']
    print("Cart ID" + str(randomCartId))

    print("COMPLETED CB: >> " + str(data))


    chat_id = update.effective_message.chat_id
    #cart_sum = db.cart.aggregate([ {'$group': {'_id:' null, 'TotalAmount': {'$sum': '$Price' }}} ])
    #cart_agg = db.cart.aggregate([{'$group' : {'_id': null, order_sum : {'$sum': "$Price"}}}])
    cart_id = ""
    total = ""
    pipe = [
                    { '$match': { str(user_id): '$UserOrderId' } },
                    { '$group': { '_id': None, total: { '$sum': '$Price' } }}
                ]
    cart_aggr = db.cart.aggregate(pipeline=pipe)
    
    pipeline = [
        {"$unwind": "$UserOrderId"},
        {"$group": {"_id": "$UserOrderId", "sum": {"$sum": "$Price"}}}
    ]

    cursor = db.cart.aggregate(pipeline)

    # convert cursor to list and print

    result = list(cursor)
    
    total_order_payment = ""
    for doc in result:
        print("DOC >> " + str(doc))
        print("TOTAL SUM: >>>>>>" + str(doc['sum']))
        total_order_payment = doc['sum']

    context.user_data['Total'] = total_order_payment
    ordered_items_list = " \U00002668 Your Complete Order Details: \U00002668 \n\n"
    cursor_cart = db.cart.find({})
    OrderId = randomCartId
    UserId = user_id
    FullName = user_data['fullname']
    UserName = user_data['username']

    user_comment = user_data["UserComment"]
    user_address = user_data["UserAddress"]


    if context.user_data["UserPhone"] != "":
        user_phone = user_data["UserPhone"]
    if context.user_data["UserLocation"] != "":
        user_location = user_data["UserLocation"]

    ordered_items_list += "Order Number: " + str(OrderId) + "\n" + "Order Name: " + str(FullName) + "\n"
    ordered_items_list += "User Name: " + str(UserName) + "\n" + "UserID: " + str(UserId) + "\n\n"
    ordered_items_list += "\U0000260E Telephone: " + str(user_phone) + "\n \U0001F697 Address: " + str(user_address) + "\n\U0001F4AC Notes: " + str(user_comment) + "\n\n"
    ordered_items_list += " \U00002668 Ordered Items: \U00002668 \n\n"
    
    # clear the first cart CreateRecord
    #result = db.cart.find_one_and_delete({"CartId": randomCartId})

    for cur in cursor_cart:
        if cur['UserOrderId'] == user_id: 
            
            item_name = str(cur['Order'])
            item_price = cur['Price']
            ordered_items_list += " \U00002705 " + str(item_name) + " " + str(item_price) + " $ \n"

        else:
            print("Error Something happened, maybe the cart or user are not created!!")

    cursor2 = db.cart.find({"CartId":randomCartId, "UserOrderId":{"$exists": True}},{'Order': 1, 'Price':1, '_id':0})

    for c2 in cursor2:
        print("CURSOR2 >> " + str(c2['Order']) + " " + str(c2['Price']))
    
    
    ordered_items_list +=  "\n Total: " + str(total_order_payment) + " $ \n"
    print("ORDER LIST TOTAL: " + str(ordered_items_list))
    
    reply_text = emojize(ordered_items_list)

    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U00002716 Cancel")
    completed_text = emojize(" \U00002611 Approve")

    product_keyboard =  [[InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_done")]]
    product_keyboard = list(product_keyboard)
    reply_markup_complete = InlineKeyboardMarkup(product_keyboard)

    #query.edit_message_text(reply_text, reply_markup=reply_markup_complete)
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_text, reply_markup=reply_markup_complete)
    return states.FIRST

