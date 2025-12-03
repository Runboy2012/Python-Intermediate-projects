import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from dotenv import find_dotenv, load_dotenv

# Главная асинхронная функция
async def main():
    await dsp.start_polling(bot)

# Находим наш .env файл и подгружаем переменные оттуда (в нашем случае один лишь токен бота).
load_dotenv(find_dotenv())

# Создать экземпляры классов Bot и Dispatcher.
bot = Bot(token=os.getenv('TOKEN'))
dsp = Dispatcher()

# Это обработчик(handler) команды "/start".
@dsp.message(CommandStart(aliciases=["start"]))
async def start_cmd(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    await message.answer(f"Hello, {first_name}! your id is {user_id}")

# Это обработчик всех сообщений кроме тех которых обрабатывают другие хендлеры
@dsp.message()
async def echo(message: types.Message):
    text = message.text
    await message.answer(text)

# Это та самая строчка кода которая запустить нашего бота
asyncio.run(main())
