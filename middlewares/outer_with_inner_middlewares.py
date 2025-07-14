from random import randint
from typing import Any, Callable, Dict, Awaitable
from datetime import datetime
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
# внешняя Мидлварь, которая достаёт внутренний айди юзера из какого-то стороннего сервиса
class UserInternalIdMiddleware(BaseMiddleware):

    # Метод, который вызывается при обработке события
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],  # Хэндлер для обработки события
            event: TelegramObject,  # Событие, которое мы обрабатываем (например, сообщение)
            data: Dict[str, Any],  # Словарь с данными, который можно изменять
    ) -> Any:
        user = data["event_from_user"]  # Получаем информацию о пользователе из словоря дата по тегу event_from_user

        data["internal_id"] = self.get_internal_id(user.id)  # Генерируем случайное число и добавляем его в словарь дата по тегу internal_id
        return await handler(event, data)  # Вызываем следующий хэндлер с обновленными данными

    # Метод для генерации случайного числа (индификатора)
    def get_internal_id(self, user_id: int) -> int:
        # Генерируем случайное число в диапазоне от 100_000_000 до 900_000_000 и добавляем к нему id пользователя
        return randint(100_000_000, 900_000_000) + user_id


# Внутренняя мидлварь, которая вычисляет "счастливый месяц" пользователя
class HappyMonthMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        # Получаем значение внутреннего идентификатора из предыдущей мидлвари
        internal_id: int = data["internal_id"]
        current_month: int = datetime.now().month

        # Проверяем, деля рандомно сгенерированый айди целочислено на месяц является ли он корректным месяцом
        # если да то возвращается True
        # если нет то возвращается False
        is_happy_month: bool = (internal_id % 12) == current_month

        # Сохраняем результат проверки (True или False) в словаре data по тегу is_happy_month
        data["is_happy_month"] = is_happy_month

        # Вызываем хэндлер передовая сообщения и измененный словарь data для использования его тегов в условной конструкции
        return await handler(event, data)









