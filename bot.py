import asyncio
from aiogram import Bot, Dispatcher
from handlers import bot_messages,user_commands,questionaire,group_commands,events_in_group,admin_changes_in_group
from handlers import how_users,bot_in_group
from callbacks import pagination
from middlewares.check_sub import CheckSubscription
from middlewares.antiflood import  AntiFloodMiddleware
from middlewares.outer_with_inner_middlewares import UserInternalIdMiddleware
from middlewares.flags_on_middlewares import ChatActionMiddleware
from Picture_pogination import FFFF
from config_reader import config
# новое
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import logging
async def main():
    bot = Bot(
        # новое
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(
            parse_mode=ParseMode.HTML
        )
    )
                    # ВКЛЮЧАЕМ УПРАВЛЕНИЕ РОУТЕРАМИ
    dp = Dispatcher(maintenance_mode=True)
    logging.basicConfig(level=logging.INFO)
    dp.update.outer_middleware(UserInternalIdMiddleware())
    dp.message.middleware(CheckSubscription())
    dp.message.middleware(ChatActionMiddleware())
    dp.message.middleware(AntiFloodMiddleware())
    dp.include_routers(
        bot_in_group.router,
        how_users.router3,
        group_commands.router,
        # добавили еще роутер
        user_commands.maintenance_router,
        FFFF.maintenance_router2,
        user_commands.router,
        pagination.router,
        questionaire.router,
        bot_messages.router,
        events_in_group.router,
        admin_changes_in_group.router

    )
    # сохраняем в переменнную всех админов из указанного айди чата
    admins = await bot.get_chat_administrators(-1002213553426)
    # тут мы перебираем всех администраторов из списка `admins` и сохраняем каждого админа как уникального
    admin_ids = {admin.user.id for admin in admins}
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, admins = admin_ids)

if __name__ == "__main__":
    asyncio.run(main())
