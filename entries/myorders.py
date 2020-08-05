from lib import deco
from lib.database import db
from emoji import emojize
from pprint import pprint
from time import sleep

@deco.restricted
@deco.conversation_command_handler("myorders", pass_user_data=True)
def myorders(update, context):
    chat_id = update.effective_message.chat_id
    #user_id = context.user_data['user_id']
    order_id = context.user_data['CartId']
    user_id = update.message.from_user.id
    username = update.message.from_user.username   
    
    update.message.reply_text(user_id)
    result = db.completed.find({})
    val = ""
    orders_msg = emojize( "\U0000200F <b> שלום {} להלן רשימת ההזמנות שביצעתם: </b>\n\n".format(username))
    update.message.reply_text(orders_msg, parse_mode='HTML')
    
    # Initialize some vars
    fullname = ""
    item = ""
    price = ""
    total_sum = ""
    msg = ""
    for user in result:
        if user_id == user["UserId"]:
        
            for keys in user.keys(): 

                msg += str(keys) + " : " + str(user[keys])
            """if user_id == user[keys]:
                #print ('{', keys, ":" , user[keys] , '}' )

                
                print(msg)
                sleep(1)
            else:
                #update.message.reply_text("לא נמצאו רשומות בהמתנה!")
                pass"""
    msgs = [msg[i:i + 4096] for i in range(0, len(msg), 4096)]
    for text in msgs:
        #update.message.reply_text(text=text)
        update.message.reply_text(text, parse_mode='HTML')
