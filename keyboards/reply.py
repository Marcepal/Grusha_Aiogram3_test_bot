from aiogram import types
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
# это кнопка: вектарина,опрос,голосование
    KeyboardButtonPollType,
    ReplyKeyboardRemove,

)
from aiogram.utils.keyboard import (
    ReplyKeyboardBuilder
)
main = ReplyKeyboardMarkup(
    keyboard=[
        [
            #эти кнопки будут на первом ряду
            KeyboardButton(text="регистрация"),
            KeyboardButton(text="о нас")
        ],
        [
            #эти кнопки будут на втором ряду
            KeyboardButton(text="ссылки на нас"),
            KeyboardButton(text="зашифрованое послание ивану")
            # убрали чтобы бот работал в группе
            # новое(узнает айди группы или пользователя котороых скиныли)
            # KeyboardButton(text="узнать айди премиум пользователя",request_user=types.KeyboardButtonRequestUser(request_id=1, user_is_premium=True)),
            # KeyboardButton(text="узнать айди группы",request_chat=types.KeyboardButtonRequestChat(request_id=2,chat_is_channel=False,chat_is_forum=True))

        ]
    ],
    # этот параметр делает размер кнопок маленькими
    resize_keyboard=True,
    # этот параметр делает так чтобы наша клавиатура скрывалась после первого использования ,но она не удаляется и мы сможем пользоваться ею
    one_time_keyboard=True,
    # этот параметр после активации делает так чтобы в поле ввода отображался текст
    input_field_placeholder="Выберите действие из меню",
    # если мы добавили бота в канал или в группу этот параметр делает так что если пользователь вызывает клавиатуру то она видна только ему,false позволит всем видеть клаву
    selective=True)

spec = ReplyKeyboardMarkup(
    keyboard=[
        [
            #эти кнопки будут на первом ряду
            KeyboardButton(text="о боте"),
            KeyboardButton(text="об Иване")
        ],
        [
            #эти кнопки будут на втором ряду
            KeyboardButton(text="назад")
        ]
    ],
    resize_keyboard=True,
    selective=True
)
# инициализируем метод ReplyKeyboardRemove() в переменную которую будем обьявлять в questionaire
rmk=ReplyKeyboardRemove()

def profile(text: str | list):
    builder = ReplyKeyboardBuilder()
    # тут проверка на тип данных (которые принимает text)
    # если наша переменая текст является типом данных str(строчка) мы должны занести ее в список
    if isinstance(text, str):
        # заносим переменую в список
        text=[text]

    [builder.button(text=txt) for txt in text]
    # one_time_keyboards = True скрывает клавиатуру после нажатия кнопки
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)