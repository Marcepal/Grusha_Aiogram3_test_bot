from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message

# класс на проверку типа чата
class ChatTypeFilter(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:  # [3]
        # если тип чата равен str (внутри которого "group", "supergroup") то значение True
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        # в остальных случаях false
        else:
            return message.chat.type in self.chat_type