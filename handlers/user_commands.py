import time

from aiogram import Router,Bot,F, html,types

from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder
)
import os

import re
from datetime import datetime
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message, FSInputFile, URLInputFile, BufferedInputFile, LinkPreviewOptions,CallbackQuery
from aiogram.utils.formatting import as_list, as_marked_section, Bold, as_key_value, HashTag
from aiogram.utils.markdown import hide_link
from aiogram.utils.media_group import MediaGroupBuilder
from aiogram.filters import Command,CommandObject,CommandStart,MagicData
from keyboards import reply
from filters.is_admin import IsAdmin
from filters.find_usernames import HasUsernamesFilter
from keyboards.fabrics import get_keyboard,get_keyboard_fab
from typing import List
from middlewares.outer_with_inner_middlewares import HappyMonthMiddleware
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.types import ChatMemberUpdated
router = Router()
maintenance_router = Router()
maintenance_router.message.filter(MagicData(F.maintenance_mode.is_(False)))
maintenance_router.callback_query.filter(MagicData(F.maintenance_mode.is_(False)))
# эта штука является внутреней мидлвари которая работает для роутеров
# и можно вешать фильтры и мидлвари именно на сам роутер не обязательно на все но тогда это уже будет внутрений мидлварь
router.message.middleware(HappyMonthMiddleware())
# закоментировал чтобы остальные фичи работали
# @router.message(
#     F.text,
#     HasUsernamesFilter()
# )
# async def message_with_usernames(
#         message: Message,
#         usernames: List[str]
# ):
#     await message.reply(
#         f'Спасибо! Обязательно подпишусь на '
#         f'{", ".join(usernames)}'
#     )

# Хэндлеры этого роутера перехватят все сообщения и колбэки,
# если maintenance_mode равен True
@maintenance_router.message()
async def any_message(message: Message):
    await message.answer("Бот в режиме обслуживания. Пожалуйста, подождите.")


@maintenance_router.callback_query()
async def any_callback(callback: CallbackQuery):
    await callback.answer(
        text="Бот в режиме обслуживания. Пожалуйста, подождите",
        show_alert=True
    )

# (команда вызывает с других символов(№,^,! и тд)
@router.message(CommandStart())
async def  start(message: Message):
    # тут reply чтобы клавиатура выходила в группах
    await message.reply(f"Добро пожаловать ",reply_markup=reply.main)


@router.message(F.text=="о боте")
# новое
                                    # показывает дату запуска бота
async def  start(message: Message):
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"{time_now}")
    await message.answer(f"данный бот создан разработчиком KLAIN в качестве теста своих знаний,написано в {added_text}")

@router.message(F.text=="об Иване")
async def  start(message: Message):
    # новое (время создание сообщения)
    # Получаем текущее время в часовом поясе ПК
    time_now = datetime.now().strftime('%H:%M')
    # Создаём подчёркнутый текст
    added_text = html.underline(f"Создано в {time_now}")
    # Отправляем новое сообщение с добавленным текстом с html подчеркиванием снизу
    await message.answer(f"макрик <u>комарик</u>\n\n{added_text}", parse_mode="HTML")

@router.message(F.text=="зашифрованое послание ивану")
async def  start(message: Message):
    # новое (сообщения с разметкой)
    await message.answer(f"ваня <u>щ</u>ищь <u>е</u>ее <u>го</u>у <u>л</u>эй")
    await message.answer("Hello, *world*\! /start", parse_mode=ParseMode.MARKDOWN_V2)
    await message.answer("Сообщение без <s>какой-либо разметки</s>", parse_mode=None)
 # новое (твое имя с разметкой)
    await message.answer(
        f"Hello, {html.bold(html.quote(message.from_user.full_name))}",
        parse_mode=ParseMode.HTML
    )



# реализовать (сообщение - требование для вступление в RGB_KLA1N и внизу ссылки c маленьким окном а также наверху сообщения твое имя с разметкой толстой )
# новое (красиво оформленное сообщение с использованием разного форматирования и смайлов)
@router.message(Command("testik"))
async def cmd_advanced_example(message: Message):
    content = as_list(
        as_marked_section(
            Bold("Success:"),
            "Test 1",
            "Test 3",
            "Test 4",
            marker="✅ ",
        ),
        as_marked_section(
            Bold("Failed:"),
            "Test 2",
            marker="❌ ",
        ),
        as_marked_section(
            Bold("Summary:"),
            as_key_value("Total", 4),
            as_key_value("Success", 3),
            as_key_value("Failed", 1),
            marker="  ",
        ),
        HashTag("#test"),
        sep="\n\n",
    )
    await message.answer(**content.as_kwargs())

# ненужно
# # новое  (передаем после команды два оргумента которые бот потом выведет)
# @router.message(Command("args"))
# async def cmd_settimer(
#         message: Message,
#         command: CommandObject
# ):
#     # Если не переданы никакие аргументы, то
#     # command.args будет None
#     if command.args is None:
#         await message.answer(
#             "Ошибка: не переданы аргументы"
#         )
#         return
#     # Пробуем разделить аргументы на две части по первому встречному пробелу
#     try:
#         delay_time, text_to_send = command.args.split(" ", maxsplit=1)
#     # Если получилось меньше двух частей, вылетит ValueError
#     except ValueError:
#         await message.answer(
#             "Ошибка: неправильный формат команды. Пример:\n"
#             "/settimer <time> <message>"
#         )
#         return
#     await message.answer(
#         "Таймер добавлен!\n"
#         f"Время: {delay_time}\n"
#         f"Текст: {text_to_send}"
#     )


# # новое(хуйня)
# @router.message(Command("help"))
# @router.message(CommandStart(
#     deep_link=True, magic=F.args == "help"
# ))
# async def cmd_start_help(message: Message):
#     await message.answer("Это сообщение со справкой")



# новое (разные ссылки (большие маленькие нету наверху внизу выбор какая ссылка отображается))
@router.message(Command("links"))
async def cmd_links(message: Message):
    # Две ссылки, которые попадут в итоговое сообщение
    links_text = (
        "https://nplus1.ru/news/2024/05/23/voyager-1-science-data"
        "\n"
        "https://t.me/telegram"
    )
    # Ссылка отключена
    options_1 = LinkPreviewOptions(is_disabled=True)
    await message.answer(
        f"Нет превью ссылок\n{links_text}",
        link_preview_options=options_1
    )

    # -------------------- #

    # Маленькое превью
    # Для использования prefer_small_media обязательно указывать ещё и url
    options_2 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_small_media=True
    )
    await message.answer(
        f"Маленькое превью\n{links_text}",
        link_preview_options=options_2
    )

    # -------------------- #

    # Большое превью
    # Для использования prefer_large_media обязательно указывать ещё и url
    options_3 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_large_media=True
    )
    await message.answer(
        f"Большое превью\n{links_text}",
        link_preview_options=options_3
    )

    # -------------------- #

    # Можно сочетать: маленькое превью и расположение над текстом
    options_4 = LinkPreviewOptions(
        url="https://nplus1.ru/news/2024/05/23/voyager-1-science-data",
        prefer_small_media=True,
        show_above_text=True
    )
    await message.answer(
        f"Маленькое превью над текстом\n{links_text}",
        link_preview_options=options_4
    )

    # -------------------- #

    # Можно выбрать, какая ссылка будет использоваться для предпосмотра,
    options_5 = LinkPreviewOptions(
        url="https://t.me/telegram"
    )
    await message.answer(
        f"Предпросмотр не первой ссылки\n{links_text}",
        link_preview_options=options_5
    )


# реализовать в боте
# новое (отправляет изображение из буфера,файла на пк,или ссылки)
# еще текст сверху в 1 изображении
@router.message(Command("images"), flags={"long_operation": "upload_video_note"})
async def upload_photo(message: Message):
#     # Сюда будем помещать file_id отправленных файлов, чтобы потом ими воспользоваться
    file_ids = []

    # Чтобы продемонстрировать BufferedInputFile, воспользуемся "классическим"
    # открытием файла через `open()`. Но, вообще говоря, этот способ
    # лучше всего подходит для отправки байтов из оперативной памяти
    # после проведения каких-либо манипуляций, например, редактированием через Pillow
    with open("buffer_emulation.jpg", "rb") as image_from_buffer:
        result = await message.answer_photo(
            BufferedInputFile(
                image_from_buffer.read(),
                filename="buffer_emulation.jpg"
            ),
            # эта штука делает текст над картинкой а не после нее
            show_caption_above_media=True,
            caption="Изображение из буфера"
        )
        file_ids.append(result.photo[-1].file_id)
#
    # Отправка файла из файловой системы
    # если копируешь путь то слеши наоборот
    image_from_pc = FSInputFile("C:/Users/ANDRE/OneDrive/Рабочий стол/111.jpg")
    result = await message.answer_photo(
        image_from_pc,
        caption="Изображение из файла на компьютере"
    )
    file_ids.append(result.photo[-1].file_id)

    # Отправка файла по ссылке
    image_from_url = URLInputFile("https://s1.1zoom.ru/big3/381/Italy_Mountains_Lake_508499.jpg")
    result = await message.answer_photo(
        image_from_url,
        caption="Изображение по ссылке"
    )
    file_ids.append(result.photo[-1].file_id)
    await message.answer("Отправленные файлы:\n"+"\n".join(file_ids))



# ненужно
# # новое (собирает 3 фотки в альбом)
# @router.message(Command("album"))
# async def cmd_album(message: Message):
#     album_builder = MediaGroupBuilder(
#         caption="Общая подпись для будущего альбома"
#     )
#     album_builder.add(
#         type="photo",
#         media=FSInputFile("C:/Users/ANDRE/OneDrive/Рабочий стол/111.jpg")
#         # caption="Подпись к конкретному медиа"
#
#     )
#     # Если мы сразу знаем тип, то вместо общего add
#     # можно сразу вызывать add_<тип>
#     album_builder.add_photo(
#         # Для ссылок или file_id достаточно сразу указать значение
#         media="https://s1.1zoom.ru/big3/381/Italy_Mountains_Lake_508499.jpg"
#     )
#     # доделать
#     album_builder.add_photo(
#         media="https://s1.1zoom.ru/big3/381/Italy_Mountains_Lake_508499.jpg"
#     )
#     await message.answer_media_group(
#         # Не забудьте вызвать build()
#         media=album_builder.build()
#     )



# не нужно
# @router.message(F.sticker)
# async def download_sticker(message: Message, bot: Bot):
#     await bot.download(
#         message.sticker,
#         # для Windows пути надо подправить
#         destination=f"C:/Users/ANDRE/OneDrive/Рабочий стол/tmp/{message.sticker.file_id}.webp"
#     )



# не нужно
# # новое(эта штука присылает лишь привью ссылки а саму ссылку скрывает)
# @router.message(Command("link"))
# async def cmd_hidden_link(message: Message):
#     await message.answer(
#         f"{hide_link('https://telegra.ph/file/562a512448876923e28c3.png')}"
#         f"Документация Telegram: *существует*\n"
#         f"Пользователи: *не читают документацию*\n"
#         f"Груша:"
#     )



# новое (если пользователь зашел в группу то бот присылает приветствие)
@router.message(F.new_chat_members)
async def somebody_added(message: Message):
    for user in message.new_chat_members:
        # проперти full_name берёт сразу имя И фамилию
        # (на скриншоте выше у юзеров нет фамилии)
        await message.reply(f"Привет, {user.full_name}")



user_data = {}


# 1
@router.message(Command("numbers"))
async def cmd_numbers(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard())


@router.message(Command("numbers_fab"))
async def cmd_numbers_fab(message: types.Message):
    user_data[message.from_user.id] = 0
    await message.answer("Укажите число: 0", reply_markup=get_keyboard_fab())

# новое(в ответ на то что мы делимся контактом или группой скидывает их айди)
@router.message(F.user_shared)
async def on_user_shared(message: types.Message):
    # новое (отвечает графически на сообщение)
    await message.reply(
        f"пользователь {message.user_shared.request_id}\nего ID: {message.user_shared.user_id}"
    )

#новое
@router.message(F.chat_shared)
async def on_user_shared(message: types.Message):
    # новое (отвечает графически на сообщение)
    await message.reply(
        f"чат {message.chat_shared.request_id}\nего ID: {message.chat_shared.chat_id}"
    )



# новое
# перед этим роутером срабатывает внутреняя мидлварь и оргументы оттуда передаются сюда
# потом они сравниваются для будущей проверки
@router.message(Command("happymonth"))
async def cmd_happymonth(
        message: Message,
        internal_id: int,
        is_happy_month: bool
):
    phrases = [f"Ваш ID в нашем сервисе: {internal_id}"]
    # если в словаре дата по тегу is_happy_month True
    if is_happy_month:
        phrases.append("Сейчас ваш счастливый месяц!")
    else:
        phrases.append("В этом месяце будьте осторожнее...")
    await message.answer(". ".join(phrases))


@router.message(Command("checkin"))
async def cmd_checkin(message: Message):
    builder = InlineKeyboardBuilder()
    builder.button(text="Я на работе!", callback_data="checkin")
    await message.answer(
        text="Нажимайте эту кнопку только по будним дням!",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data == "checkin")
async def callback_checkin(callback: CallbackQuery):
    # это срабатывает если сегодня не выходные
    await callback.answer(
        text="Спасибо, что подтвердили своё присутствие!",
        show_alert=True
    )
@router.message(Command("admin"),IsAdmin(895247719))
async def  start2(message: Message):
    # новое (сообщения с разметкой)
    await message.answer(f"с возвращением админ KLAIN_05")


# разобраться в этом коде и написать коментарии к нему

# пройти особые апдейты

# пройти платежи

# перечитать все темы из документации и код со всеми коментариями

# сделать 2 тз

# взять заказ на фрилансе

# на все дается 3 недели
















# ненужно
# закоментировал чтобы роутер выше работал
# # новое (если в сообщении есть ссылка пароль или почта бот видет их и потом выводит) (типо парсит)
# @router.message(F.text)
# async def extract_data(message: Message):
#     data = {
#         "url": "<N/A>",
#         "email": "<N/A>",
#         "code": "<N/A>"
#     }
#     entities = message.entities or []
#     for item in entities:
#         if item.type in data.keys():
#             # Неправильно
#             # data[item.type] = message.text[item.offset : item.offset+item.length]
#             # Правильно
#             data[item.type] = item.extract_from(message.text)
#     await message.reply(
#         "Вот что я нашёл:\n"
#         f"URL: {html.quote(data['url'])}\n"
#         f"E-mail: {html.quote(data['email'])}\n"
#         f"Пароль: {html.quote(data['code'])}"
#     )