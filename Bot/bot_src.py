import asyncio
import logging
import os
import sys
import shutil
from os import getenv

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.markdown import hbold

from aiogram.types import FSInputFile, URLInputFile, BufferedInputFile

# Bot token can be obtained via https://t.me/BotFather
TOKEN = '7157055794:AAEmA2Bx5LO7FNUeNHDqlBjvXhoRtS8tgH4'

# All handlers should be attached to the Router (or Dispatcher)
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`
    try:
        os.mkdir("images/"+message.from_user.username)
    except:
        pass
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!\n Для создания вашего изображения с одеждой загрузите две фотографии:\n - свою \n - одежды\n Подождите несколько минут")

"""
@dp.message()
async def echo_handler(message: types.Message) -> None:
"""
    #Handler will forward receive a message back to the sender

    #By default, message handler will handle all message types (like a text, photo, sticker etc.)
"""
    try:
        # Send a copy of the received message
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        # But not all the types is supported to be copied so need to handle it
        await message.answer("Привет!\nЯ бот, помогающий с примеркой!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.")  # Так как код работает асинхронно, то обязательно пишем await.")
 """

@dp.message(Command("special_buttons"))
async def cmd_special_buttons(message: types.Message):
    builder = ReplyKeyboardBuilder()
    # метод row позволяет явным образом сформировать ряд
    # из одной или нескольких кнопок. Например, первый ряд
    # будет состоять из двух кнопок...
    builder.row(
        types.KeyboardButton(text="Запросить геолокацию", request_location=True),
        types.KeyboardButton(text="Запросить контакт", request_contact=True)
    )
    # ... второй из одной ...
    builder.row(types.KeyboardButton(
        text="Создать викторину",
        request_poll=types.KeyboardButtonPollType(type="quiz"))
    )
    # ... а третий снова из двух
    builder.row(
        types.KeyboardButton(
            text="Выбрать премиум пользователя",
            request_user=types.KeyboardButtonRequestUser(
                request_id=1,
                user_is_premium=True
            )
        ),
        types.KeyboardButton(
            text="Выбрать супергруппу с форумами",
            request_chat=types.KeyboardButtonRequestChat(
                request_id=2,
                chat_is_channel=False,
                chat_is_forum=True
            )
        )
    )
    # WebApp-ов пока нет, сорри :(

    await message.answer(
        "Выберите действие:",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )


@dp.message(Command('Images'))
async def upload_photo(message: Message):
    # Сюда будем помещать file_id отправленных файлов, чтобы потом ими воспользоваться
    file_ids = []

    # Чтобы продемонстрировать BufferedInputFile, воспользуемся "классическим"
    # открытием файла через `open()`. Но, вообще говоря, этот способ
    # лучше всего подходит для отправки байтов из оперативной памяти
    # после проведения каких-либо манипуляций, например, редактированием через Pillow
    with open("images/jacket.jpg", "rb") as image_from_buffer:
        result = await message.answer_photo(
            BufferedInputFile(
                image_from_buffer.read(),
                filename="images/jacket.jpg"
            ),
            caption="Изображение из буфера"
        )
        file_ids.append(result.photo[-1].file_id)

    # Отправка файла из файловой системы
    image_from_pc = FSInputFile("images/bad_model.jpg")
    result = await message.answer_photo(
        image_from_pc,
        caption="Изображение из файла на компьютере"
    )
    file_ids.append(result.photo[-1].file_id)

    # Отправка файла по ссылке
    image_from_url = URLInputFile("https://picsum.photos/seed/groosha/400/300")
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )
    file_ids.append(result.photo[-1].file_id)
    await message.answer("Отправленные файлы:\n"+"\n".join(file_ids))

#Скачать медиа к себе на локальную машину
@dp.message(F.photo)
async def download_photo(message: Message, bot: Bot):
    # создание папки при загрузке фотографии
    # если папки нет, то ее надо сделать
    if not(os.path.exists(f"images/{message.from_user.username}")):
        os.mkdir(f"images/{message.from_user.username}")

    await bot.download(
        message.photo[-1],
        #destination=f"/tmp/{message.photo[-1].file_id}.jpg"
        destination=f"images/{message.from_user.username}/{ (len(os.listdir('images/'+message.from_user.username)))+1}.jpg" #Место сохранения файла на локальной машине


    )


@dp.message(Command('delete'))
def delete_photo(message: Message):
    if (len(os.listdir("images/"+ message.from_user.username))) > 0:
        try:
            shutil.rmtree("images/"+message.from_user.username)
            os.mkdir("images/"+message.from_user.username)
        except Exception:
            pass



async def main() -> None:
    # Initialize Bot instance with a default parse mode which will be passed to all API calls
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    # And the run events dispatching
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())