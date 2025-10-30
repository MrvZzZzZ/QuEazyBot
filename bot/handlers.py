from database.api import exec
from database.querys import query
from quiz.quiz_data import quiz_data
from bot.service import dp, get_question, new_quiz

from aiogram.filters.command import Command
from aiogram import  types, F
from aiogram.utils.keyboard import ReplyKeyboardBuilder

@dp.callback_query(F.data.startswith("answer:"))
async def right_answer(callback: types.CallbackQuery):
    user_choice = (int)(callback.data.split(":", 1)[1])

    await callback.bot.edit_message_reply_markup(
        chat_id=callback.from_user.id,
        message_id=callback.message.message_id,
        reply_markup=None
    )
    data = await exec(query["get quiz"], (callback.from_user.id, ))
    current_question_index = (int)(data[0])
    actual_result = (int)(data[1])

    await callback.message.answer(f"Ваш ответ: {quiz_data[current_question_index]['options'][user_choice]}")

    correct_option = quiz_data[current_question_index]['correct_option']
    if user_choice == correct_option:
        await callback.message.answer("Верно!")
        actual_result += 1
    else:
        await callback.message.answer(f"Неправильно. Правильный ответ: {quiz_data[current_question_index]['options'][correct_option]}")
    
    current_question_index += 1
    await exec(query["update quiz"], (callback.from_user.id, current_question_index, actual_result))

    if current_question_index < len(quiz_data):
        await get_question(callback.message, callback.from_user.id)
    else:
        last_result = round(actual_result/len(quiz_data) * 100, 2)
        await callback.message.answer(f"Это был последний вопрос. Квиз завершен!\n\nВаш результат: {last_result}%")
        await exec(query["set result"], (last_result, callback.from_user.id))


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Начать игру"))
    builder.add(types.KeyboardButton(text="Посмотреть результат"))
    await message.answer("Добро пожаловать в квиз!", reply_markup=builder.as_markup(resize_keyboard=True))

@dp.message(F.text=="Посмотреть результат")
async def cmd_result(message: types.Message):
    res = await exec(query["get result"], (message.from_user.id, ))
    last_result = res[0]
    if last_result == None or last_result == 0:
        await message.answer("Вы еще не прошли Quiz =(")
    else: 
        await message.answer(f"Ваш результат прошлого прохождения: {last_result}%") 

@dp.message(F.text=="Начать игру")
@dp.message(Command("quiz"))
async def cmd_quiz(message: types.Message):
    await message.answer(f"Давайте начнем квиз!")
    await new_quiz(message)

