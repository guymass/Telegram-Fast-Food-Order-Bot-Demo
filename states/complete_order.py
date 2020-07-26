from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
from random import choice
from settings import CHATID
cbs = "completed"

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True,  pass_update_queue=True)
def complete_order(update, context):
    query = update.callback_query
    data = update.callback_query.data
    user_id = query.from_user.id
    user_data = context.user_data

    randomCartId = user_data['CartId']
    print("Cart ID" + str(randomCartId))

    print("COMPLETED CB: >> " + str(data))


    chat_id = update.effective_message.chat_id
    #cart_sum = db.cart.aggregate([ {'$group': {'_id:' null, 'TotalAmount': {'$sum': '$Price' }}} ])
    #cart_agg = db.cart.aggregate([{'$group' : {'_id': null, order_sum : {'$sum': "$Price"}}}])
    cart_id = ""
    total = ""
    pipe = [
                    { '$match': { randomCartId: '$CartId' } },
                    { '$group': { '_id': None, total: { '$sum': '$Price' } }}
                ]
    cart_aggr = db.cart.aggregate(pipeline=pipe)
    
    pipeline = [
        {"$unwind": "$CartId"},
        {"$group": {"_id": "$CartId", "sum": {"$sum": "$Price"}}}
    ]

    cursor = db.cart.aggregate(pipeline)

    # convert cursor to list and print

    result = list(cursor)
    
    total_order_payment = ""
    for doc in result:
        print("DOC >> " + str(doc))
        print("TOTAL SUM: >>>>>>" + str(doc['sum']))
        total_order_payment = doc['sum']

    """pipe = [{'$group': {'_id': None, 'total': {'$sum': '$Price'}}}]
    cart_aggr = db.cart.aggregate(pipeline=pipe)

    total_order_payment = ""
    for doc in db.cart.aggregate(pipeline=pipe):
        print(doc)
        total_order_payment = doc['total']"""

    context.user_data['Total'] = total_order_payment
    ordered_items_list = " \U00002668 Your Order Details: \U00002668 \n\n"
    cursor_cart = db.cart.find({})
    OrderId = randomCartId
    UserId = user_id
    FullName = user_data['fullname']
    UserName = str(user_data['username'])

    ordered_items_list += "Order Number " + str(OrderId) + "\n" + "Order Name " + str(FullName) + "\n"
    ordered_items_list += "Username " + str(UserName) + "\n" + "UserId " + str(UserId) + "\n\n"
    ordered_items_list += " \U00002668 Items Ordered\U00002668 \n\n"
    
    # clear the first cart CreateRecord
    #result = db.cart.find_one_and_delete({"CartId": randomCartId})

    for cur in cursor_cart:
        if cur['UserOrderId'] == user_id: 
            
            item_name = str(cur['Order'])
            item_price = cur['Price']
            ordered_items_list += " \U00002705 " + str(item_name) + " $" + str(item_price)

        else:
            print("Error Something happened, maybe the cart or user are not created!!")

    cursor2 = db.cart.find({"CartId":randomCartId, "UserOrderId":{"$exists": True}},{'Order': 1, 'Price':1, '_id':0})

    for c2 in cursor2:
        print("CURSOR2 >> " + str(c2['Order']) + " " + str(c2['Price']))
    
    
    ordered_items_list +=  "\n Total Sum: $" + str(total_order_payment) + "\n"
    print("ORDER LIST TOTAL: " + str(ordered_items_list))
    
    reply_text = emojize(ordered_items_list)

    back_button = emojize(" \U000021AA Back")
    cancel_text = emojize(" \U000021AA Cancel")
    completed_text = emojize(" \U000021AA Approve")

    product_keyboard =  [[InlineKeyboardButton(back_button, callback_data="cb_back"), InlineKeyboardButton(cancel_text, callback_data="cancel")],[InlineKeyboardButton(completed_text, callback_data="cb_done")]]
    product_keyboard = list(product_keyboard)
    reply_markup_complete = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_complete)

    return states.FIRST

