from pathlib import Path
from aiogram import Router
from aiogram.types import Message, CallbackQuery, FSInputFile, InputMediaPhoto
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData
from aiogram.utils.keyboard import InlineKeyboardBuilder

maintenance_router2 = Router()

# Фабрика callback‑данных
class PaginateCb(CallbackData, prefix="pg"):
    action: str  # 'next' или 'prev'
    page: int

# Автоматический поиск изображений
def get_image_paths():
    # Папка с изображениями лежит рядом с файлом скрипта
    current_dir = Path(__file__).resolve().parent
    images_dir = current_dir / "images for FFFF"  # папка без пробелов и без C:/
    images_dir.mkdir(parents=True, exist_ok=True)  # создаём, если её нет

    return sorted([
        str(p) for p in images_dir.iterdir()
        if p.is_file() and p.suffix.lower() in ('.jpg', '.jpeg', '.png')
    ])

# Клавиатура пагинации
def pagination_keyboard(page: int, total: int):
    kb = InlineKeyboardBuilder()
    if page > 0:
        kb.button(text="⬅️ Назад", callback_data=PaginateCb(action="prev", page=page - 1).pack())
    if page < total - 1:
        kb.button(text="➡️ Вперёд", callback_data=PaginateCb(action="next", page=page + 1).pack())
    kb.adjust(2)
    return kb.as_markup()

# Команда /pictures
@maintenance_router2.message(Command("pictures"))
async def cmd_pictures(message: Message):
    image_paths = get_image_paths()
    if not image_paths:
        await message.answer("❌ Картинки не найдены.")
        return
    page = 0
    file = FSInputFile(image_paths[page])
    caption = f"Изображение {page + 1}/{len(image_paths)}"
    await message.answer_photo(
        photo=file,
        caption=caption,
        reply_markup=pagination_keyboard(page, len(image_paths))
    )

# Обработка нажатия кнопок пагинации
@maintenance_router2.callback_query(PaginateCb.filter())
async def paginate_handler(callback: CallbackQuery, callback_data: PaginateCb):
    image_paths = get_image_paths()
    page = callback_data.page
    file = FSInputFile(image_paths[page])
    caption = f"Изображение {page + 1}/{len(image_paths)}"
    media = InputMediaPhoto(media=file, caption=caption)
    await callback.message.edit_media(media=media, reply_markup=pagination_keyboard(page, len(image_paths)))
    await callback.answer()