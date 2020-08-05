from telegram.utils import helpers
from telegram.ext import Filters
from emoji import emojize
from lib import (deco, common)
from lib.database import db
import datetime

@deco.restricted
@deco.global_message_handler(Filters.photo)
@deco.conversation_message_handler(Filters.photo)
@deco.conversation_message_handler(
    Filters.document.category("video/mp4") | Filters.document.category("video") | Filters.video,
    pass_user_data=True, pass_chat_data=True, pass_update_queue=True)
def listimages(update, context):

    chat_id = update.effective_message.chat_id
    user_id = update.message.from_user.id
    message_types = ['photo', 'video']
    upload_date = update.effective_message.date
    caption = update.message.caption
    username = update.effective_message.from_user.first_name
    message_types = ['audio', 'game', 'document',
                     'photo', 'sticker', 'video/mp4', 'video', 'voice']
    mt = helpers.effective_message_type(update.message)
    if mt in message_types:
        print("MESSAGE TYPE >>>>>: " + str(mt))
    media = []
    userId = str(user_id)
    date = str(upload_date)
    document = ""
    cap = str(caption)

    m = update.message
    if m.video:
        file_id = m.video.file_id
        document = "video/mp4"
    elif m.document:
        if m.document.mime_type == 'video/mp4':
            file_id = m.document.file_id
            document = "document"

    if document in message_types:
        #file_id = update.message.video.file_id

        current_time = datetime.datetime.utcnow()

        m = update.message
        if document == 'video/mp4':
            file_id = m.video.file_id
        elif document == 'document':
            file_id = m.document.file_id
        print("FILE-ID >>>>> " + str(file_id))
        text = update.effective_message.caption
        userId = str(user_id)
        date = str(upload_date)
        vidId = str(file_id)
        cap = str(text)
        video_owner = str(username)
        randomNum = common.randStr(N=10)
        video_code = str(userId+randomNum)
        image_type = str(document)
        userId = str(user_id)
        date = str(upload_date)
        imgId = str(file_id)
        cap = str(caption)

        cursor = db.images.find({})
        for img in cursor:
            if img['ImageCode'] == "p1":
                image_code = "p2"
                pass
            elif img['ImageCode'] == "p2":
                image_code = "p3"
                pass
            elif img['ImageCode'] == "p3":
                image_code = "p4"
                pass
            elif img['ImageCode'] == "p4":
                image_code = "p1"
                pass
            elif img['ImageCode'] == "":
                image_code = "p1"

        if db.images.count() == 0:
            image_code = "p1"
            document = "photo"

        video_item = {
            "UserId": user_id,
            "ImageId": imgId,
            "FileType": image_type,
            "ImageText": cap,
            "ImageCode": image_code,
            "ImageDate": date
        }

        db.images.insert_one(video_item)

        video_details = emojize("\U0000200F תאריך העלאה: "+str(upload_date)+"\n"
                                + "על ידי: "+"@"+str(username)+"\n"
                                + "קוד: "+str(video_code)+"\n----------------\n")
        video_details += cap

        if document == 'video/mp4':

            context.bot.send_video(
                chat_id, video=file_id, caption=video_details, parse_mode='HTML')
            user_msg = "הסרטון עודכן בהצלחה!"
            update.message.reply_text(user_msg)
        elif document == 'document':
            context.bot.send_document(
                chat_id, document=file_id, caption=video_details, parse_mode='HTML')
            user_msg = "הסרטון עודכן בהצלחה!"
            update.message.reply_text(user_msg)

        pass
    else:
        context.bot.send_message(
            chat_id, text="\U0000200F משהו קרה והקובץ לא נשמר, נסו שנית.")
        pass

    if caption == "logo":
        res = db.logo.delete_many({})
        update.message.reply_text(" תמונת לוגו התקבלה!")
        file_id = update.message.photo[0].file_id
        current_time = datetime.datetime.utcnow()
        context.bot.send_message(chat_id, str(upload_date))
        context.bot.send_message(chat_id, file_id)
        context.bot.send_photo(chat_id, file_id)
        context.bot.send_message(chat_id, str(caption))

        cursor = db.images.find({})
        for img in cursor:
            if img['ImageCode'] == "logo":
                res = db.logo.delete_many({})
                pass
            elif db.images.count() == 0:
                image_code = "logo"

        image_code = "logo"
        image_type = str(document)
        userId = str(user_id)
        date = str(upload_date)
        imgId = str(file_id)
        cap = str(caption)
        imageItem = {
            "UserId": user_id,
            "ImageId": imgId,
            "ImageText": cap,
            "FileType": image_type,
            "ImageCode": image_code,
            "ImageDate": date

        }
        db.logo.insert_one(imageItem)

    else:
        file_id = update.message.photo[0].file_id
        current_time = datetime.datetime.utcnow()
        context.bot.send_message(chat_id, str(upload_date))
        context.bot.send_message(chat_id, file_id)
        context.bot.send_photo(chat_id, file_id)
        context.bot.send_message(chat_id, str(caption))
        document = ""
        cursor = db.images.find({})
        for img in cursor:
            if img['ImageCode'] == "p1":
                image_code = "p2"
                document = "photo"
                pass
            elif img['ImageCode'] == "p2":
                image_code = "p3"
                document = "photo"
                pass
            elif img['ImageCode'] == "p3":
                image_code = "p4"
                document = "photo"
                pass
            elif img['ImageCode'] == "p4":
                image_code = "p1"
                document = "photo"
                pass
            elif img['ImageCode'] == "":
                image_code = "p1"
                document = "photo"

        if db.images.count() == 0:
            image_code = "p1"
            document = "photo"

        m = update.message
        if m.video:
            file_id = m.video.file_id
            document = "video/mp4"
        elif m.document:
            if m.document.mime_type == 'video/mp4':
                file_id = m.document.file_id
                document = "document"

        image_type = str(document)
        userId = str(user_id)
        date = str(upload_date)
        imgId = str(file_id)
        cap = str(caption)
        imageItem = {
            "UserId": user_id,
            "ImageId": imgId,
            "FileType": image_type,
            "ImageText": cap,
            "ImageCode": image_code,
            "ImageDate": date

        }
        db.images.insert_one(imageItem)
