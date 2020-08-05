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
    completed_order_message += "\U00002139 מספר הזמנה: " + str(OrderId) + "\n\U00002139 " + "שם המזמין: " + str(FullName) + "\n\U00002139 " + "שם משתמש: " + str(UserName) + "\n\U00002139 " + "מספר זיהוי: " + str(UserId) + "\n\n"
    completed_order_message += "\U0000260E מספר טלפון: " + str(user_phone) + "\n \U0001F697 כתובת משלוח: " + str(user_address) + "\n\U0001F4AC הערות: " + str(user_comment) + "\n\n"
    completed_order_message += "\U0001F514 להלן רשימת הפריטים שהוזמנו: \n"
   
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
            completed_order_message += "\U00002705 שם פריט: " + str(ItemOrdered) + " " + str(ItemPrice) + " ש\"ח \n"

        else:
            print("Error Something happened, maybe the cart or user are not created!!")
    
    #Add the total sum
    doc = db.completed.find_one_and_update(
    {"OrderId": OrderId},
    {"$set":
        {"TotalSum": int(total_user_data)}
    },upsert=True
    )
    completed_order_message += "\U0001F4B3 סך הכל לתשלום: " + str(total_user_data) + " ש\"ח \n\n"
    completed_order_message += "\U0001F336     \U0001F336     \U0001F336     \U0001F336     \U0001F336     \U0001F336\n\n"

    context.bot.send_message(chat_id=CHATID, text=completed_order_message)

    
    print("TOTAL ORDER PAYMENT == " + str(total_user_data))
    #print("COMPLETE ORDER PAYMENT == " + str(complete_order_payment))
    
    reply_text = " \U0001F4CB  הזמנתכם התקבלה במערכת! אנו ניצור עמכם קשר בקרוב להשלמת פרטי התשלום ומשלוח, אנא שימו לב להודעה מאיתנו בצאט של הטלאגרם. \n"

    done_keyboard = []
    done_keyboard =  [[InlineKeyboardButton("סיום", callback_data="cb_end")]]
    done_keyboard = list(done_keyboard)
    reply_markup_done = InlineKeyboardMarkup(done_keyboard)
    query.edit_message_text(reply_text, reply_markup=reply_markup_done)
    return states.FIRST

