import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from functions import subjects_keyboard_creator, one_file_keyboard_creator, refrences_keyboard_creator, content_keyboard_creator, forward_file

from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.environ.get("BOT_TOKEN")

with open("./files_data.json", "r", encoding="utf-8") as files_data_json:
    files_data = json.load(files_data_json)

CHANNEL_ID = -1002468726141
CHANNEL_USERNAME = "@medicology_abzums"


async def is_user_member(channel_username: str, user_id: int, context):
    try:
        member = await context.bot.get_chat_member(chat_id=channel_username, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


async def start(update: Update, context=ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    is_member = await is_user_member(
        channel_username=CHANNEL_USERNAME, user_id=user_id, context=context)

    if not is_member:
        keyboard = [
            [InlineKeyboardButton(
                "کانال مدیکولوژی", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=chat_id,
            text="اگر میخوای از ربات استفاده کنی، لطفا اول داخل کانالمون عضو شو ❤",
            reply_markup=reply_markup
        )
        return

    reply_markup = content_keyboard_creator(contents=files_data)

    if update.message:
        await update.message.reply_text("جزوه میخوای یا رفرنس؟", reply_markup=reply_markup)

    if update.callback_query:
        query = update.callback_query
        # await query.answer()
        await context.bot.edit_message_text(text="جزوه میخوای یا رفرنس؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
        # await query.edit_message_text("برای چه درسی جزوه میخوای؟", reply_markup=reply_markup)


async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = update.effective_user.id
    chat_id = update.effective_chat.id

    is_member = await is_user_member(
        channel_username=CHANNEL_USERNAME, user_id=user_id, context=context)

    if not is_member:
        keyboard = [
            [InlineKeyboardButton(
                "کانال مدیکولوژی", url=f"https://t.me/{CHANNEL_USERNAME.lstrip('@')}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await context.bot.send_message(
            chat_id=chat_id,
            text="اگر میخوای از ربات استفاده کنی، لطفااول داخل کانالمون عضو شو ❤",
            reply_markup=reply_markup
        )
        return

    if query.data == 'start':
        await start(update=update, context=context)

    if query.data.split('_')[1] == '-1' or query.data.split('_')[1] == '[]':
        await context.bot.send_message(
            chat_id=chat_id,
            text="متاسفانه فایل مورد نظرت هنوز داخل ربات قرار نگرفته ولی اگر عنوانش توی ربات هست یعنی در آینده (دور یا نزدیک!) در ربات قرار میگیره ❤️\n\nاما اگر موردی بود که کلا توی ربات نبود و بهش نیاز داشتی (از جزوه و رفرنس و آموزش گرفته تا هر چیز دیگه ای) به من پیام بده:\n@MehrshadChKh",
        )
        return

    if query.data.split('_')[0] == "back":
        if query.data.split('_')[1] == "contents":
            reply_markup = content_keyboard_creator(files_data)
            await context.bot.edit_message_text(text="جزوه میخوای یا رفرنس؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
            return

        if query.data.split('_')[1] == "pamphlets":
            print(query.data.split('_')[1])
            reply_markup = subjects_keyboard_creator(
                files_data["pamphlets"]["subjects"], content="pamphlets")
            await context.bot.edit_message_text(text="نوع محتوا: جزوه \n\n برای چه درسی جزوه میخوای؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
            # await query.edit_message_text("برای چه درسی جزوه میخوای؟", reply_markup=reply_markup)
            return

        if query.data.split('_')[1] == "refrences":
            reply_markup = subjects_keyboard_creator(
                files_data["refrences"]["subjects"], content="refrences")
            await context.bot.edit_message_text(text="نوع محتوا: رفرنس \n\n رفرنس چه درسی رو میخوای؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
            # await query.edit_message_text("برای چه درسی جزوه میخوای؟", reply_markup=reply_markup)
            return

        if query.data.split('_')[1] == "tutorials":
            reply_markup = subjects_keyboard_creator(
                files_data["tutorials"]["subjects"], content="tutorials")
            await context.bot.edit_message_text(text="نوع محتوا: آموزش مدیکولوژی \n\n آموزش های چه درسی رو میخوای؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
            # await query.edit_message_text("برای چه درسی جزوه میخوای؟", reply_markup=reply_markup)
            return

    if query.data.split('_')[0] == "contents":
        if query.data.split('_')[1] == "pamphlets":
            reply_markup = subjects_keyboard_creator(
                files_data["pamphlets"]["subjects"], content="pamphlets")
            await context.bot.edit_message_text(text="نوع محتوا: جزوه \n\n برای چه درسی جزوه میخوای؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)

        if query.data.split('_')[1] == "refrences":
            reply_markup = subjects_keyboard_creator(
                files_data["refrences"]["subjects"], content="refrences")
            await context.bot.edit_message_text(text="نوع محتوا: رفرنس \n\n رفرنس چه درسی رو میخوای؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)

        if query.data.split('_')[1] == "tutorials":
            reply_markup = subjects_keyboard_creator(
                files_data["tutorials"]["subjects"], content="tutorials")
            await context.bot.edit_message_text(text="نوع محتوا: آموزش مدیکولوژی \n\n آموزش های چه درسی رو میخوای؟", message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)

    if query.data.split('_')[0] == "pamphlets":
        reply_markup = one_file_keyboard_creator(
            query.data.split('_')[1], "pamphlets")
        await context.bot.edit_message_text(text=f'نوع محتوا: جزوه\nدرس: {files_data["pamphlets"]["subjects"][query.data.split("_")[1]]["name"]}\n\nخب حالا مبحث مورد نظرتو انتخاب کن:', message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
        # await query.edit_message_text(text=f'درس: {files_data[query.data.split("_")[1]]["name"]}\n\nخب حالا مبحث مورد نظرتو انتخاب کن:', reply_markup=reply_markup)
        return

    if query.data.split('_')[0] == "refrences":
        reply_markup = refrences_keyboard_creator(query.data.split('_')[1])
        await context.bot.edit_message_text(text=f'نوع محتوا: رفرنس\nرفرنس: {files_data["refrences"]["subjects"][query.data.split("_")[1]]["name"]}\n\nانگلیسی یا ترجمه شده؟', message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
        # await query.edit_message_text(text=f'درس: {files_data[query.data.split("_")[1]]["name"]}\n\nخب حالا مبحث مورد نظرتو انتخاب کن:', reply_markup=reply_markup)
        return

    if query.data.split('_')[0] == "tutorials":
        reply_markup = one_file_keyboard_creator(
            query.data.split('_')[1], "tutorials")
        await context.bot.edit_message_text(text=f'نوع محتوا: آموزش مدیکولوژی\nدرس: {files_data["tutorials"]["subjects"][query.data.split("_")[1]]["name"]}\n\nخب حالا مبحث مورد نظرتو انتخاب کن:', message_id=query.message.message_id, chat_id=chat_id, reply_markup=reply_markup)
        # await query.edit_message_text(text=f'درس: {files_data[query.data.split("_")[1]]["name"]}\n\nخب حالا مبحث مورد نظرتو انتخاب کن:', reply_markup=reply_markup)
        return

    if query.data.split('_')[0] == "send-file":
        file_id = query.data.split('_')[1]
        chat_id = query.message.chat.id

        await forward_file(file_id=file_id, chat_id=chat_id,
                           channel_id=CHANNEL_ID, context=context)
        return


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_buttons))

app.run_polling()
