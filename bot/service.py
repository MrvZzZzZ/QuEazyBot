from database.api import exec
from database.querys import query
from quiz.quiz_data import quiz_data

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import Dispatcher, Bot, types
from config import API_TOKEN

dp = Dispatcher()

async def start_polling():
    bot = Bot(token=API_TOKEN)
    await dp.start_polling(bot)

def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    for i, option in enumerate(answer_options):
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=f"answer:{i}")
        )

    builder.adjust(1)
    return builder.as_markup()

async def new_quiz(message):
    user_id = message.from_user.id
    current_question_index = 0
    actual_result = 0
    await exec(query["update quiz"], (user_id, current_question_index, actual_result))
    await get_question(message, user_id)

async def get_question(message, user_id):
    data = await exec(query["get quiz"], (user_id, ))
    current_question_index = data[0]
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)
