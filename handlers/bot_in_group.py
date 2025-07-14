from aiogram import Router,Bot,F
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, IS_NOT_MEMBER, MEMBER, ADMINISTRATOR
from aiogram.types import ChatMemberUpdated
# просто в качестве примеров:

# # Не забываем импорты:
# from aiogram.filters.chat_member_updated import \
#     ChatMemberUpdatedFilter, KICKED, LEFT, MEMBER, \
#     RESTRICTED, ADMINISTRATOR, CREATOR
#
# @router.my_chat_member(
#     ChatMemberUpdatedFilter(
#         member_status_changed=
#         (KICKED | LEFT | -RESTRICTED)
#         >>
#         (+RESTRICTED | MEMBER | ADMINISTRATOR | CREATOR)
#     )
# )

#
# # Немного другие импорты
# from aiogram.filters.chat_member_updated import \
#     ChatMemberUpdatedFilter, IS_NOT_MEMBER, IS_MEMBER
#
# @router.my_chat_member(
#     ChatMemberUpdatedFilter(
#         member_status_changed=
#         IS_NOT_MEMBER >> IS_MEMBER
#     )
# )

# # И ещё меньше импортов
# from aiogram.filters.chat_member_updated import \
#     ChatMemberUpdatedFilter, JOIN_TRANSITION
#
# @router.my_chat_member(
#     ChatMemberUpdatedFilter(
#         member_status_changed=JOIN_TRANSITION
#     )
# )
router = Router()

# проверка на тип чата
router.chat_member.filter(F.chat.type.in_({"group", "supergroup"}))
# словарь
chats_variants = {
    "group": "группу",
    "supergroup": "супергруппу"
}


# Не удалось воспроизвести случай добавления бота как Restricted,
# поэтому примера с ним не будет

# роутер если бота добавили в группу в качестве администратора
@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> ADMINISTRATOR
    )
)
async def bot_added_as_admin(event: ChatMemberUpdated):
    # Самый простой случай: бот добавлен как админ.
    # Легко можем отправить сообщение
    await event.answer(
        text=f"Привет! Спасибо, что добавили меня в "
             f'{chats_variants[event.chat.type]} "{event.chat.title}" '
             f"как администратора. ID чата: {event.chat.id}"
    )

# роутер если бота добавили как участника
@router.my_chat_member(
    ChatMemberUpdatedFilter(
        member_status_changed=IS_NOT_MEMBER >> MEMBER
    )
)
async def bot_added_as_member(event: ChatMemberUpdated, bot: Bot):
    # Вариант посложнее: бота добавили как обычного участника.
    # Но может отсутствовать право написания сообщений, поэтому заранее проверим.
    chat_info = await bot.get_chat(event.chat.id)
    if chat_info.permissions.can_send_messages:
        await event.answer(
            text=f"Привет! Спасибо, что добавили меня в "
                 f'{chats_variants[event.chat.type]} "{event.chat.title}" '
                 f"как обычного участника. ID чата: {event.chat.id}"
        )
    else:
        print("Как-нибудь логируем эту ситуацию")