from aiogram import Router, F,types
from handlers.user_commands import user_data
from keyboards.fabrics import get_keyboard,get_keyboard_fab,NumbersCallbackFactory
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest
router = Router()
# после нажатия инлайн кнопок их команды которые мы прописали отправляются и тут обрабатываются

# # роутеры которые срабатывают на кнопку с фексироваными значениеми

# @router.callback_query(NumbersCallbackFactory.filter(F.action == "change"))
# # функция изменения числа
# async def callbacks_num_change_fab(
#         callback: types.CallbackQuery,
#         callback_data: NumbersCallbackFactory
# ):
#     # получаем текущее значение юзера которое равно 0
#     user_value = user_data.get(callback.from_user.id, 0)
#     # плюсуем текущее значение юзера с значением присущего кнопке
#     user_data[callback.from_user.id] = user_value + callback_data.value
#     # вызываем функцию апдейт
#     await update_num_text_fab(callback.message, user_value + callback_data.value)
#     # ответ числом которое вышло в итоге
#     await callback.answer()


# # Нажатие на кнопку "подтвердить"
# @router.callback_query(NumbersCallbackFactory.filter(F.action == "finish"))
# async def callbacks_num_finish_fab(callback: types.CallbackQuery):
#     # Текущее значение
#     user_value = user_data.get(callback.from_user.id, 0)
#
#     await callback.message.edit_text(f"Итого: {user_value}")
#     await callback.answer()



@router.callback_query(NumbersCallbackFactory.filter())
# функция обновления числа только на экране
async def callbacks_num_change_fab(
        callback: types.CallbackQuery,
        callback_data: NumbersCallbackFactory
):
    # получает текущее значение 0
    user_value = user_data.get(callback.from_user.id, 0)
    # Если число нужно изменить
    if callback_data.action == "change":
        # к текущему значению прибавляем значение которое присуще нашей кнопке
        user_data[callback.from_user.id] = user_value + callback_data.value
        await update_num_text_fab(callback.message, user_value + callback_data.value)
    # Если число нужно зафиксировать
    else:
        await callback.message.edit_text(f"Итого: {user_value}")
    await callback.answer()

# функция обновления текста сообщения
async def update_num_text_fab(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard_fab()
        )






# 3
async def update_num_text(message: types.Message, new_value: int):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Укажите число: {new_value}",
            reply_markup=get_keyboard()
        )

# 5
@router.callback_query(F.data.startswith("num_"))
async def callbacks_num(callback: types.CallbackQuery):
    user_value = user_data.get(callback.from_user.id, 0)
    action = callback.data.split("_")[1]

    if action == "incr":
        user_data[callback.from_user.id] = user_value+1
        await update_num_text(callback.message, user_value+1)
    elif action == "decr":
        user_data[callback.from_user.id] = user_value-1
        await update_num_text(callback.message, user_value-1)
    elif action == "finish":
        await callback.message.edit_text(f"Итого: {user_value}")

    await callback.answer()