from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import (Poll, ParseMode, KeyboardButton, KeyboardButtonPollType,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, PollAnswerHandler, PollHandler, MessageHandler,
                          Filters)
from telegram.utils.helpers import mention_html
from emoji import emojize
from lib import (common, deco, states)
from lib.database import db
from random import choice
from settings import CHATID
from time import sleep

cbs = "cb_extra_manager"

@deco.run_async
@deco.register_state_callback(states.FIRST, pattern=f'^cb_({cbs})$', pass_user_data=True, pass_chat_data=True, pass_update_queue=True)
def extra_manager(update, context):

    query = update.callback_query
    data = update.callback_query.data
    user_data = context.user_data
    user_id = user_data['user_id']
    tortia_selection = context.user_data['TortiaSelection']
    randomCartId = context.user_data['CartId']
    product_keyboard = []


    payload_message_id = context.user_data['TortiaFirstPollMessageId']
    print("FIRST SENT PAYLOAD MSG ID: ######### " + str(payload_message_id))
    first_poll_id = context.user_data['FirstSaladPollId']
    print("FIRST POLL ID %%%%%%%: " + str(first_poll_id))
    extra_poll_message_id = context.user_data['ExtraPollMessageId']
    extra_poll_id = context.user_data['ExtraPollId']
    print("EXTRA MSG ID: >>>> " + str(extra_poll_message_id))
    print("EXTRA POLL ID: >>> " + str(extra_poll_id))

    first_poll_data = context.bot_data[first_poll_id]
    print("FIRST POLL DATA >>: " + str(first_poll_data))
    sec_poll_data = context.bot_data[extra_poll_id]
    print("FIRST POLL DATA >>: " + str(sec_poll_data))


    """Summarize a users poll vote"""
    #answer = update.poll_answer
    
    answer = context.bot_data[poll_id]["answers"]
    poll_id = answer.poll_id

    print(answer)
    try:
        questions = context.bot_data[poll_id]["questions"]
    # this means this poll answer update is from an old poll, we can't do our answering then
    except KeyError:
        return
    selected_options = answer.option_ids
    answer_string = ""
    for question_id in selected_options:
        if question_id != selected_options[-1]:
            answer_string += questions[question_id] + " and "
        else:
            answer_string += questions[question_id]
    
    ויuser_mention = mention_html(update.effective_user.id, update.effective_user.full_name)
    
    context.bot.send_message(context.bot_data[poll_id]["chat_id"],
                             "{} feels {}!".format(user_mention, answer_string),
                             parse_mode=ParseMode.HTML)
    context.bot_data[poll_id]["answers"] += 1
    # Close poll after three participants voted
    if context.bot_data[poll_id]["answers"] == 1:
        context.bot.stop_poll(context.bot_data[poll_id]["chat_id"],
                              context.bot_data[poll_id]["message_id"])


    for answer in answers:
        if answer.voter_count == 1:
            ret = answer.text
            print("ANSWER POLL:" + str(ret))

    sleep(1)
    reply_text = emojize("\n \U0000200F בחירתכם {} התקבלה.")

    #back_button = emojize("\U0000200F \U000021AA חזרה")
    approve_salad_first_selection = emojize("\U0000200F \U000021AA אשרו בחירה")
    cancel_text = emojize("\U0000200F \U00002716 ביטול")
    #completed_text = emojize("\U0000200F \U00002611 הזמן עכשיו")

    product_keyboard +=  [[InlineKeyboardButton(approve_salad_first_selection, callback_data="cb_approve_first_salads"), InlineKeyboardButton(cancel_text, callback_data="cancel")]]
    product_keyboard = list(product_keyboard)
    reply_markup_tortia_salad = InlineKeyboardMarkup(product_keyboard)

    query.edit_message_text(reply_text, reply_markup=reply_markup_tortia_salad)
    return states.FIRST
