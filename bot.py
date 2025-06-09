import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
from functions import subjects_keyboard_creator, topics_keyboard_creator, forward_file

import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")

with open("./files_data.json", "r", encoding="utf-8") as files_data_json:
    files_data = json.load(files_data_json)

CHANNEL_ID = -1002468726141
CHANNEL_USERNAME = "@Medicology_ABZUMS"


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

    reply_markup = subjects_keyboard_creator(files_data)

    if update.message:
        await update.message.reply_text("برای چه درسی جزوه میخوای؟", reply_markup=reply_markup)

    if update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text("برای چه درسی جزوه میخوای؟", reply_markup=reply_markup)


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

    if query.data.split('_')[1] == '-1':
        await context.bot.send_message(
            chat_id=chat_id,
            text="متاسفانه جزوه این مبحث هنوز داخل ربات قرار نگرفته ولی به زودی قرار میگیره ❤\n\nاگر درس یا مبحثی کلا توی ربات نیست و به جزوه اش نیاز داری یا اینکه جزوه خوبی داری که میخوای به اشتراک بذاری که داخل ربات قرار بگیره، به من پیام بده:\n@MehrshadChKh",
        )
        return

    if query.data.split('_')[0] == "back":
        if query.data.split('_')[1] == "subjects":
            reply_markup = subjects_keyboard_creator(files_data)
            await query.edit_message_text("برای چه درسی جزوه میخوای؟", reply_markup=reply_markup)
            return

    if query.data.split('_')[0] == "topics":
        reply_markup = topics_keyboard_creator(query.data.split('_')[1])
        await query.edit_message_text(f'درس: {files_data[query.data.split("_")[1]]["name"]}\n\nخب حالا مبحث مورد نظرتو انتخاب کن:', reply_markup=reply_markup)
        return

    if query.data.split('_')[0] == "send-file":
        file_id = int(query.data.split('_')[1])
        chat_id = query.message.chat.id

        await forward_file(file_id=file_id, chat_id=chat_id,
                           channel_username=CHANNEL_USERNAME, context=context)
        return


app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(handle_buttons))

app.run_polling()
print("Bot started...")
