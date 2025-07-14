from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

sub_channel = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="подписаться на канал", url="https://t.me/KLAIN055")

        ]
    ]
)


links = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="YouTube", url="https://youtu.be/@klAi_05"),
# "t.me://RGB_KLA1N" ссылка такого формата перекидывает нас в браузер
# "tg://resolve?domain=RGB_KLA1N" ссылка такого формата перекидывает на к пользователю внутри телеграмма
            InlineKeyboardButton(text="Telegram", url="tg://resolve?domain=RGB_KLA1N")

        ]
    ]
)

