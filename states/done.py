from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
from settings import CHATID


@deco.run_async
@deco.register_state_callback(states.FIRST, pattern="^cb_done$", pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def done(update, context):
    query = update.callback_query
    data = update.callback_query.data
    user_data = context.user_data

    OrderId = user_data['CartId']
    UserId = user_data['user_id']
    FullName = user_data['fullname']
    UserName = '@'+str(user_data['username'])
    user_comment = user_data["UserComment"]
    user_address = user_data["UserAddress"]
    user_phone = user_data["UserPhone"]
    user_location = user_data["UserLocation"]
    total_user_data = user_data['Total']

    completed_order_message = " \U0001F336     \U0001F336     \U0001F336     \U0001F336     \U0001F336     \U0001F336\n\n"
    completed_order_message += "\U00002139 Order Number: " + str(OrderId) + "\n\U00002139 " + "Order Name: " + str(FullName) + "\n\U00002139 " + "User Name: " + str(UserName) + "\n\U00002139 " + "User ID: " + str(UserId) + "\n\n"
    completed_order_message += "\U0000260E Telephone: " + str(user_phone) + "\n \U0001F697 Address: " + str(user_address) + "\n\U0001F4AC Notes: " + str(user_comment) + "\n\n"
    completed_order_message += "\U0001F514 Your Complete Order Details: \n"
   
    completed_order = []
    order_item = {
        "OrderId":OrderId,
        "FullName": FullName,
        "UserName": UserName,
        "UserId": UserId,
        "UserComment":user_comment,
        "UserAddress":user_address,
        "UserPhone":user_phone,
        "UserLocation":user_location,
        
    }
    result = db.completed.insert_one(order_item)
    i=0
    cursor_cart = db.cart.find({})
    for cur in cursor_cart:
        if cur['UserOrderId'] == UserId and cur['CartId'] == OrderId:
            i += 1
            ItemOrdered = cur['Order']
            ItemPrice = cur['Price']

            Item = "Item" + "{}".format(i)
            Price = "Price" + "{}".format(i)

            doc = db.completed.find_one_and_update(
            {"OrderId": OrderId},
            {"$set":
                {Item: ItemOrdered, Price: int(ItemPrice)}
            },upsert=True)
            completed_order_message += "\U00002705 Item Name: " + str(ItemOrdered) + " " + str(ItemPrice) + " $ \n"

        else:
            print("Error Something happened, maybe the cart or user are not created!!")
    
    #Add the total sum
    doc = db.completed.find_one_and_update(
    {"OrderId": OrderId},
    {"$set":
        {"TotalSum": int(total_user_data)}
    },upsert=True
    )
    completed_order_message += "\U0001F4B3 Total: " + str(total_user_data) + " $ \n\n"
    completed_order_message += "\U0001F336     \U0001F336     \U0001F336     \U0001F336     \U0001F336     \U0001F336\n\n"

    context.bot.send_message(chat_id=CHATID, text=completed_order_message)

    
    print("TOTAL ORDER PAYMENT == " + str(total_user_data))
    #print("COMPLETE ORDER PAYMENT == " + str(complete_order_payment))
    
    reply_text = " \U0001F4CB Your order was received and we will contact oyu shortly to complete the transaction details (DEMO no charge here!)\n"

    done_keyboard = []
    done_keyboard =  [[InlineKeyboardButton("Done", callback_data="cb_end")]]
    done_keyboard = list(done_keyboard)
    reply_markup_done = InlineKeyboardMarkup(done_keyboard)
    query.edit_message_text(reply_text, reply_markup=reply_markup_done)
    return states.FIRST

