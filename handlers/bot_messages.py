from aiogram import Router, F
from aiogram.types import Message
from keyboards import reply,inline
# , builders,fabrics)



router = Router()

@router.message()
async def echo(message:Message):
    msg=message.text
    if msg == "о нас":
        await message.answer("выберете:",reply_markup=reply.spec)
    elif msg == "назад":
        await message.answer("Вы перешли в главное меню!",reply_markup=reply.main)
    elif msg == "ссылки на нас":
        await message.answer("наши ссылки",reply_markup=inline.links)

