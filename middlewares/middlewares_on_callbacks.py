from datetime import datetime  # Импортируем модуль для работы с датой и временем
from typing import Any, Callable, Dict, Awaitable  # Импортируем типы данных для аннотаций типов

from aiogram import BaseMiddleware  # Импортируем базовый класс мидлвари из aiogram
from aiogram.types import CallbackQuery, TelegramObject  # Импортируем типы объектов из aiogram


class WeekendCallbackMiddleware(BaseMiddleware):

    # Определяем метод is_weekend, который проверяет, является ли сегодня выходной.
    def is_weekend(self) -> bool:
        # datetime.utcnow().weekday() возвращает день недели от 0 до 6,
        # где 0 - это понедельник, а 6 - воскресенье.
        # Мы проверяем, если сегодня суббота (5) или воскресенье (6), возвращаем True.
        # Если не выходной, то возвращаем False.
        return datetime.utcnow().weekday() in (5, 6)

    # Определяем асинхронный метод call, который будет вызываться каждый раз,
    # когда происходит событие (например, нажатие кнопки).
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        # Если событие не является CallbackQuery (например, это не нажатие кнопки),
        # то мы просто пропускаем это событие и даем ему идти дальше, к основному обработчику.
        # это нужно чтобы мидлварь реагировало лишь на калбек
        if not isinstance(event, CallbackQuery):
            return await handler(event, data)

        # Если сегодня не выходной (not True)
        # то продолжаем обработку события в основном обработчике.
        if not self.is_weekend():
            return await handler(event, data)

        # Если сегодня выходной (суббота или воскресенье), мы не хотим обрабатывать
        # это событие дальше. Вместо этого мы показываем пользователю сообщение.
        await event.answer(
            "Какая работа? Завод остановлен до понедельника!",  # Сообщение пользователю
            show_alert=True  # Показываем это сообщение в виде всплывающего окна (alert)
        )
        return  # Завершаем обработку события и не передаем его дальше