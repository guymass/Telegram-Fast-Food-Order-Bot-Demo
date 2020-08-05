from lib import deco
from emoji import emojize

@deco.restricted
@deco.run_async
@deco.conversation_command_handler("admin")
def admin(update, context):
    chat_id = update.effective_message.chat_id
    user_id = update.message.from_user.id
    msg = emojize("\U0000200F \U0001F53D להלן רשימת הפקודות של הבוט \U0001F53D\n\n" +
                  "\U0001f505 להתחלת הזמנה הקלידו \U000025C0 /start\n\n" +
                  "\U0001f505 לצפייה בהזמנות בהמתנה כתבו את הפקודה \U000025C0 /getlist\n\n" +
		  "\U0001f505 למחיקת רשומות כתבו \U000025C0 /purge\n" +
                  "\U0001f505 לצפייה במוצרים הזמינים לבוט כתבו את הפקודה \U000025C0 /products\n\n" +
                  "\U0001f505 לסגירת ההזמנה יש  כתוב את פקודת \U000025C0 /setitem והמספר הטלפון של המזמין\n פקודה זו תעדכן את מצב ההזמנה - ל- <b>Delivered</b>\n\n" +
                  "\U0001f505 לקבלת עדכון מצב של כל ההזמנות שבוצעו יחד עם סך כולל יש לכתוב \U000025C0 /total\n\n" +
                  "\U0001f505 עלמנת לעדכן תמונות מוצר חדשים לבוט יש פשוט להעלות תמונה לבוט והוא יארגן אותן במקום \n\n כאשר רוצים להחליף תמונות יש לרשום פקודת /clear שתמחוק את התמונות הישנות.\n\n" +
                  "\U0001f505 עלמנת לעדכן תמונת פתיחה\לוגו יש לשלוח תמונה עם הכיתוב \U000025C0 logo בלבד\n\n"
                  "\U0001f505 עלמנת לראות שוב את הודעת העזרה כתבו \U000025C0 /admin")
    context.bot.send_message(chat_id, msg, parse_mode='HTML')
