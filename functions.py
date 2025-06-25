from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import json
import ast

with open("./files_data.json", "r", encoding="utf-8") as files_data_json:
    files_data = json.load(files_data_json)


def add_back_button(keyboard, back_to_where):
    if len(keyboard[-1]) == 1:
        keyboard[-1] = [InlineKeyboardButton(
            "منوی قبلی ⬅", callback_data=f"back_{back_to_where}"), keyboard[-1][0],]
    elif len(keyboard[-1]) == 2:
        keyboard.append([InlineKeyboardButton(
            "منوی قبلی ⬅", callback_data=f"back_{back_to_where}")])

    return keyboard


def content_keyboard_creator(contents):
    keyboard_one_row = [
        InlineKeyboardButton(contents[content]["name"],
                             callback_data=f'contents_{contents[content]["callback_data"]}')
        for content in contents
    ]

    keyboard_two_rows = [keyboard_one_row[i:i+2]
                         for i in range(0, len(keyboard_one_row), 2)]

    reply_markup = InlineKeyboardMarkup(keyboard_two_rows)
    return reply_markup


def subjects_keyboard_creator(subjects_data, content):
    keyboard_one_row = [
        InlineKeyboardButton(text=subjects_data[subject]["name"],
                             callback_data=f'send-file_{subjects_data[subject]["files"]}' if "files" in subjects_data[subject] else f'{content}_{subjects_data[subject]["callback_data"]}')
        for subject in subjects_data
    ]

    keyboard_two_rows = [keyboard_one_row[i:i+2]
                         for i in range(0, len(keyboard_one_row), 2)]

    final_keyboard = add_back_button(
        keyboard=keyboard_two_rows, back_to_where="contents")
    reply_markup = InlineKeyboardMarkup(final_keyboard)
    return reply_markup


def pamphlets_keyboard_creator(subject_data):
    topics = files_data["pamphlets"]["subjects"][subject_data]["topics"]

    keyboard_one_row = [
        InlineKeyboardButton(topics[topic]["name"], callback_data=f'send-file_{topics[topic]["file_id"]}') for topic in topics
    ]

    keyboard_two_rows = [keyboard_one_row[i:i+2]
                         for i in range(0, len(keyboard_one_row), 2)]

    final_keyboard = add_back_button(
        keyboard=keyboard_two_rows, back_to_where="pamphlets")

    reply_markup = InlineKeyboardMarkup(final_keyboard)
    return reply_markup


def refrences_keyboard_creator(subject_data):
    refrences = files_data["refrences"]["subjects"][subject_data]

    keyboard_one_row = [
        InlineKeyboardButton(
            "انگلیسی", callback_data=f'send-file_{refrences["english"]["files"]}'),
        InlineKeyboardButton(
            "ترجمه", callback_data=f'send-file_{refrences["translated"]["files"]}')
    ]

    keyboard_two_rows = [keyboard_one_row[i:i+2]
                         for i in range(0, len(keyboard_one_row), 2)]

    final_keyboard = add_back_button(
        keyboard=keyboard_two_rows, back_to_where="refrences")

    reply_markup = InlineKeyboardMarkup(final_keyboard)
    return reply_markup


async def forward_file(chat_id, channel_id, file_id, context):
    file_id_evaluated = ast.literal_eval(file_id)

    if isinstance(file_id_evaluated, int):
        await context.bot.forward_message(
            chat_id=chat_id, from_chat_id=channel_id, message_id=file_id_evaluated)

    if isinstance(file_id_evaluated, list):
        for file in file_id_evaluated:
            await context.bot.forward_message(
                chat_id=chat_id, from_chat_id=channel_id, message_id=file)

    keyboard = [[InlineKeyboardButton('استارت', callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(chat_id=chat_id, text="بفرما اینم از جزوه یا رفرنس مد نظرت ✌\n\nاگر جزوه یا رفرنس دیگه ای مد نظرته، دوباره ربات رو استارت کن ❤", reply_markup=reply_markup)
