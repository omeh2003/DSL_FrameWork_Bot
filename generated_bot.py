import logging
import random
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.utils import executor

import config

logging.basicConfig(level=logging.INFO)

API_TOKEN = 'API-TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())


async def START_send_message(message: types.Message):
    await message.reply("Choose an option:", parse_mode=ParseMode.HTML)


async def START_show_keyboard(message: types.Message):
    keyboard_markup = types.ReplyKeyboardMarkup(row_width=2)

    button = types.KeyboardButton("Show random number")
    keyboard_markup.add(button)

    button = types.KeyboardButton("Tell a joke")
    keyboard_markup.add(button)

    await message.reply("Choose an option:", reply_markup=keyboard_markup)


# Register message handlers

@dp.message_handler(commands=['start'])
async def start_command_handler(message: types.Message):
    await START_send_message(message)

    await START_show_keyboard(message)


import random


async def RANDOM_NUMBER_send_random_number(message: types.Message):
    random_number = random.randint(1, 100)
    await message.reply(f"Here's a random number between 1 and 100: {random_number}", parse_mode=ParseMode.HTML)


@dp.message_handler(lambda message: message.text.lower() == 'show random number')
async def random_number_handler(message: types.Message):
    await RANDOM_NUMBER_send_random_number(message)


async def RANDOM_NUMBER_back_to_start(message: types.Message):
    await START_send_message(message)
    await START_show_keyboard(message)


@dp.message_handler(lambda message: message.text.lower() == 'back to main menu')
async def back_to_start_handler(message: types.Message):
    await RANDOM_NUMBER_back_to_start(message)


@dp.message_handler(commands=['random_number'])
async def random_number_command_handler(message: types.Message):
    await RANDOM_NUMBER_send_random_number(message)

    await RANDOM_NUMBER_back_to_start(message)


import random


async def JOKE_send_joke(message: types.Message):
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the chicken cross the road? To get to the other side!",
        "Why couldn't the bicycle stand up by itself? Because it was two-tired!",
        "Why do we never tell secrets on a farm? Because the potatoes have eyes and the corn has ears!",
        "What's orange and sounds like a parrot? A carrot!"
    ]

    selected_joke = random.choice(jokes)
    await message.reply("Here's a funny joke: {}".format(selected_joke), parse_mode=ParseMode.HTML)


@dp.message_handler(lambda message: message.text.lower() == 'tell a joke')
async def joke_handler(message: types.Message):
    await JOKE_send_joke(message)


async def JOKE_back_to_start(message: types.Message):
    await START_show_keyboard(message)


@dp.message_handler(lambda message: message.text.lower() == 'back to main menu' and current_state == "JOKE")
async def joke_back_to_start_handler(message: types.Message):
    await JOKE_back_to_start(message)


@dp.message_handler(commands=['joke'])
async def joke_command_handler(message: types.Message):
    await JOKE_send_joke(message)

    await JOKE_back_to_start(message)


async def on_start(dp):
    await bot.send_message(chat_id=config.ADMIN_ID, text='Bot has been started')


async def on_shutdown(dp):
    await bot.send_message(chat_id=config.ADMIN_ID, text='Bot has been stopped')

    await dp.storage.close()
    await dp.storage.wait_closed()

    await bot.session.close()


if __name__ == '__main__':
    from aiogram import executor

    executor.start_polling(dp, on_startup=on_start, on_shutdown=on_shutdown)
