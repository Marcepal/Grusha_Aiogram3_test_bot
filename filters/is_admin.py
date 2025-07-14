# импортируем чтобы в этот фильтр можно было передовать не только один айдишник но и несколько
from typing import List
from aiogram.filters import BaseFilter
                            # фильтры можно делать не только к message но и к callbackquery
from aiogram.types import Message

class IsAdmin(BaseFilter):

    def __init__(self,user_ids: int | List[int])-> None:
        self.user_ids = user_ids

    async def __call__(self,message: Message)->bool:
        if isinstance(self.user_ids,int):
            return message.from_user.id==self.user_ids
        return message.from_user.id in self.user_ids