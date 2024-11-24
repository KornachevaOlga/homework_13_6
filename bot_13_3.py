from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = ''
bot = Bot(token = api)
dp = Dispatcher(bot, storage= MemoryStorage())

# kb = ReplyKeyboardMarkup()
# button = KeyboardButton(text='Расчитать')
# button2 = KeyboardButton(text='Информация')
# kb.add(button)
# kb.add(button2)
kb = ReplyKeyboardMarkup(resize_keyboard=True).add(
    KeyboardButton(text='Рассчитать'),
    KeyboardButton(text='Информация'))

kbi = InlineKeyboardMarkup(resize_keyboard=True).add(
    InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories'),
    InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas'))



class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.message_handler(commands= ['start'])
async def start(message):
    await message.answer('Я бот, помогающий твоему здоровью!', reply_markup = kb)

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию', reply_markup = kbi)

@dp.callback_query_handler(text = 'formulas')
async def get_formulas(call):
    await call.message.answer('Формула Миффлина-Сан Жеора для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    await message.answer('Введите свой рост')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    data = await state.get_data()
    await message.answer('Введите свой вес')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def  send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    age = int(data['age'])
    weight = int(data['weight'])
    growth = int(data['growth'])
    #for i, j in data:


    calories_wom = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Ваша норма калорий: {calories_wom}')
    await state.finish()

@dp.message_handler()
async def all_massages(message):
    #print('Введите команду /start, чтобы начать общение.')
    #await message.answer(message.text.upper())
    await message.answer('Привет! Введите команду /start, чтобы начать общение')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
# from aiogram import Bot, Dispatcher, executor, types
# from aiogram.contrib.fsm_storage.memory import MemoryStorage
# from aiogram.dispatcher.filters.state import State, StatesGroup
# import asyncio
#
# api = ''
# bot = Bot(token=api)
# dp = Dispatcher(bot=bot, storage=MemoryStorage())
#
# class UserState(StatesGroup):
#     age = State()
#     growth = State()
#     weight = State()
#
# @dp.message_handler(text=['Calories', 'Калории', 'Ккал'])
# async def set_age(message):
#     await message.answer('Введите свой возраст:')
#     await UserState.age.set()
#
# @dp.message_handler(state=UserState.age)
# async def set_growth(message, state):
#     await state.update_data(age=message.text)
#     await message.answer('Введите свой рост (см):')
#     await UserState.growth.set()
#
# @dp.message_handler(state=UserState.growth)
# async def set_weight(message, state):
#     await state.update_data(growth=message.text)
#     await message.answer('Введите свой вес (кг):')
#     await UserState.weight.set()
#
# @dp.message_handler(state=UserState.weight)
# async def send_calories(message, state):
#     await state.update_data(weight=message.text)
#     data = await state.get_data()
#
#     try:
#         age = float(data['age'])
#         weight = float(data['weight'])
#         growth = float(data['growth'])
#     except:
#         await message.answer(f'Не могу конвертировать введенные значения в числа.')
#         await state.finish()
#         return
#
#     # Упрощенный вариант формулы Миффлина-Сан Жеора:
#     # для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5
#     calories_man = 10 * weight + 6.25 * growth - 5 * age + 5
#     #для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161
#     calories_wom = 10 * weight + 6.25 * growth - 5 * age - 161
#     await message.answer(f'Норма (муж.): {calories_man} ккал')
#     await message.answer(f'Норма (жен.): {calories_wom} ккал')
#     await state.finish()
#
# if __name__ == '__main__':
#     executor.start_polling(dp, skip_updates=True)


