from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import json

with open("./files_data.json", "r", encoding="utf-8") as files_data_json:
    files_data = json.load(files_data_json)


def subjects_keyboard_creator(subjects_data):
    keyboard_one_row = [
        InlineKeyboardButton(subjects_data[subject]["name"],
                             callback_data=f'topics_{subjects_data[subject]["callback_data"]}')
        for subject in subjects_data
    ]

    keyboard_two_rows = [keyboard_one_row[i:i+2]
                         for i in range(0, len(keyboard_one_row), 2)]

    reply_markup = InlineKeyboardMarkup(keyboard_two_rows)
    return reply_markup


def topics_keyboard_creator(subject_data):
    topics = files_data[subject_data]["topics"]

    keyboard_one_row = [
        InlineKeyboardButton(topics[topic]["name"], callback_data=f'send-file_{topics[topic]["file_id"]}') for topic in topics
    ]

    keyboard_two_rows = [keyboard_one_row[i:i+2]
                         for i in range(0, len(keyboard_one_row), 2)]

    if len(keyboard_two_rows[-1]) == 1:
        keyboard_two_rows[-1] = [InlineKeyboardButton(
            "منوی قبلی ⬅", callback_data='back_subjects'), keyboard_two_rows[-1][0],]
    elif len(keyboard_two_rows[-1]) == 2:
        keyboard_two_rows.append([InlineKeyboardButton(
            "منوی قبلی ⬅", callback_data='back_subjects')])

    reply_markup = InlineKeyboardMarkup(keyboard_two_rows)
    return reply_markup


async def forward_file(chat_id, channel_username, file_id, context):
    await context.bot.forward_message(
        chat_id=chat_id, from_chat_id=channel_username, message_id=file_id)

    keyboard = [[InlineKeyboardButton('استارت', callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text="بفرما اینم از جزوه مد نظرت ✌\n\nاگر جزوه دیگه ای مد نظرته، دوباره ربات رو استارت کن ❤", reply_markup=reply_markup)
