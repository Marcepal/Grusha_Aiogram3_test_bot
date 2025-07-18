# from aiogram import F, Router
# from aiogram.filters.chat_member_updated import \
#     ChatMemberUpdatedFilter, KICKED, LEFT, \
#     RESTRICTED, MEMBER, ADMINISTRATOR, CREATOR
# from aiogram.types import ChatMemberUpdated
#
# from config_reader import config
#
# router = Router()
# router.chat_member.filter(F.chat.id == -1002213553426)
#
#
# @router.chat_member(
#     ChatMemberUpdatedFilter(
#         member_status_changed=
#         (KICKED | LEFT | RESTRICTED | MEMBER)
#         >>
#         (ADMINISTRATOR | CREATOR)
#     )
# )
# # до этого мы уже создали множество admins в bot.py
# #
# # тут мы добавили множество`admins`, которое может хранить только "целые числа" (1, 2, 3 ну или айдишники) и не может хранить два одинаковых числа(айди админов).
# # мы создаем именно admins как множество так как элементы внутри него неизменны
# # значит если админа повысили до админа множество не примет снова тот же айдишник
#
# # set[int]-эта штука указывает какие значения хранит в себе admins(в данном случае айдишники из цифр)
# async def admin_promoted(event: ChatMemberUpdated, admins: set[int]):
#     admins.add(event.new_chat_member.user.id)
#     await event.answer(
#         f"{event.new_chat_member.user.first_name} "
#         f"был(а) повышен(а) до Администратора!"
#     )
#
#
# @router.chat_member(
#     ChatMemberUpdatedFilter(
#         # Обратите внимание на направление стрелок
#         # Или можно было поменять местами объекты в скобках
#         member_status_changed=
#         (KICKED | LEFT | RESTRICTED | MEMBER)
#         <<
#         (ADMINISTRATOR | CREATOR)
#     )
# )
# async def admin_demoted(event: ChatMemberUpdated, admins: set[int]):
#     admins.discard(event.new_chat_member.user.id)
#     await event.answer(
#         f"{event.new_chat_member.user.first_name} "
#         f"был(а) понижен(а) до обычного юзера!"
#     )