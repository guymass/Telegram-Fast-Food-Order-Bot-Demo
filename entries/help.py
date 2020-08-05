from lib import deco
from emoji import emojize

@deco.conversation_command_handler("help")
def help(update, context):
    chat_id = update.effective_message.chat_id
    msg = emojize(" להלן רשימת הפקודות של הבוט של באביס\n" +
                                "להתחלת הזמנה הקלידו /start\n" +
                                "להצגת ההזמנה שלכם כתבו /myorders \n" +
                                "עלמנת לראות שוב את הודעת העזרה כתבו /help")
    context.bot.send_message(chat_id, msg)
