from typing import Callable,Awaitable,Dict, Any

from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache

class AntiFloodMiddleware(BaseMiddleware):
    def __init__(self,time_limit: int=1) -> None:
        self.limit = TTLCache(maxsize=10_000,ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message,Dict[str,Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.chat.id in self.limit:
            return
        else:
            self.limit[event.chat.id] = None
        return await handler(event,data)

# мидлвари и фильтры можно вешать на 1 роутер не обязательно на все

# handler — собственно, объект хэндлера, который будет выполнен.
# Имеет смысл только для inner-мидлварей, т.к. outer-мидлварь ещё не знает, в какой хэндлер попадёт апдейт.

# event — тип Telegram-объекта, который обрабатываем. Обычно это Update, Message, CallbackQuery или InlineQuery (но не только)
# . Если точно знаете, какого типа объекты обрабатываете, смело пишите, например, Message вместо TelegramObject.

# data — связанные с текущим апдейтом данные: FSM, переданные доп. поля из фильтров, флаги (о них позже) и т.д.
# В этот же data мы можем класть из мидлварей какие-то свои данные, которые будут доступны в виде аргументов в хэндлерах (так же, как в фильтрах).


# (Message, CallbackQuery и т.д.) являются апдейтами











# более простая версия
# import asyncio
# from typing import Any, Callable, Dict, Awaitable
# from aiogram import BaseMiddleware
# from aiogram.types import TelegramObject
#
# class SlowpokeMiddleware(BaseMiddleware):
#     def __init__(self, sleep_sec: int):
#         self.sleep_sec = sleep_sec
#
#     async def __call__(
#             self,
#             handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
#             event: TelegramObject,
#             data: Dict[str, Any],
#     ) -> Any:
#         # Ждём указанное количество секунд и передаём управление дальше по цепочке
#         # (это может быть как хэндлер, так и следующая мидлварь)
#         await asyncio.sleep(self.sleep_sec)
#         result = await handler(event, data)
#         # Если в хэндлере сделать return, то это значение попадёт в result
#         print(f"Handler was delayed by {self.sleep_sec} seconds")
#         return result