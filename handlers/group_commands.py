# тут обработчик команд только в группах
from aiogram import Router
from aiogram.enums.dice_emoji import DiceEmoji
from aiogram.types import Message
from aiogram.filters import Command

from filters.chat_type import ChatTypeFilter

router = Router()

# перед выполнением команды роутер отправляет данные в chat_type на проверку передавая список туда
@router.message(
    ChatTypeFilter(chat_type=["group", "supergroup"]),
    Command(commands=["dice"]),
)
async def cmd_dice_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.DICE)


@router.message(
    ChatTypeFilter(chat_type=["group", "supergroup"]),
    Command(commands=["basketball"]),
)
async def cmd_basketball_in_group(message: Message):
    await message.answer_dice(emoji=DiceEmoji.BASKETBALL)