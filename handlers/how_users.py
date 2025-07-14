from aiogram import F, Router
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED
from aiogram.filters.command import \
    Command
from aiogram.types import ChatMemberUpdated, Message


# особые апдейты важно!

# ссылка на обьяснения статусов и переходов статусов для телеграмм бота
#https://docs.aiogram.dev/en/dev-3.x/dispatcher/filters/chat_member_updated.html

# my_chat_member. Здесь всё, что касается непосредственно бота, либо ЛС юзера с ботом:
# (раз)блокировки бота юзером в ЛС, добавление бота в группу или канал, удаление оттуда, изменение прав бота
# и его статуса в разных чатах и т.д.
#
#
# chat_member. Содержит все изменения состояния пользователей в группах и каналах,
# где бот состоит в качестве администратора: приход/уход юзеров в группы, подписки/отписки в каналах,
# изменение прав и статусов пользователей, назначение/снятие админов и многое другое.


router3 = Router()
router3.my_chat_member.filter(F.chat.type == "private")
router3.message.filter(F.chat.type == "private")

# Исключительно для примера!
# В реальной жизни используйте более надёжные
# источники айди юзеров
users = {111, 222}

# если пользователь имеет статус (кикнут) то удаляем этого юзера из списка юзиров
@router3.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=KICKED)
)
async def user_blocked_bot(event: ChatMemberUpdated):
    users.discard(event.from_user.id)

# если пользователь имеет статус (участник) то добовляем юзера в список
@router3.my_chat_member(
    ChatMemberUpdatedFilter(member_status_changed=MEMBER)
)
async def user_unblocked_bot(event: ChatMemberUpdated):
    users.add(event.from_user.id)

# при вызове этой команды пользователь автоматом зачисляется в список юзеров которые пользуются этим ботом
@router3.message(Command("one"))
async def cmd_start(message: Message):
    await message.answer("Hello")
    users.add(message.from_user.id)

# при вызове этой команды выводится список юзеров которые пользуются этим ботом
@router3.message(Command("users"))
async def cmd_users(message: Message):
    await message.answer("\n".join(f"• {user_id}" for user_id in users))

