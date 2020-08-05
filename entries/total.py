from lib import deco
from lib.database import db
from emoji import emojize
from pprint import pprint
from time import sleep

@deco.restricted
@deco.conversation_command_handler("total")
def total(update, context):
    chat_id = update.effective_message.chat_id
    _id = ""
    total = ""

    result = db.completed.aggregate([ {"$group": {"_id": 0, "TotalAmount": {"$sum": "$TotalSum"}}} ] )
    pprint(result)

    for res in result:
        print("TotalSumResult >>: " + str(res['TotalAmount']))
        total += str(res['TotalAmount'])
    """for r in result:
        status = r["Status"]
        if status == "Delivered":
            total_orders.append(r["Quantity"])
            msg = emojize("☑️ הזמנה שסופקה:" + "\n" + str(r["UserId"]) + "\n" + str(r["UserName"]) + "\n" + str(r["FullName"]) + "\n" + "קוד מוצר: " + str(r["Product"]) + "\n" + "כמות: " +str(r["Quantity"]))
            msg2 = emojize("\n" + str(r["Mobile"]) + "\n" + str(r["Address"]) + "\n" + str(r["Message"]) + "\n\U0001F973 " + str(r["Status"]) + " \U0001F973\n" + str(r["Date"]))
            context.bot.send_message(chat_id, msg+msg2)

    for i in range(0, result.count()):
        sum = sum + total_orders[i]"""

    msg = emojize(" סיכום סך הזמנות {} ש\"ח ".format(total))
    print(msg)
    context.bot.send_message(chat_id, msg)
