# тут классы машины состояния где у нас записаны наши переменные состояния внутри этих классов
from aiogram.fsm.state import StatesGroup,State
# это отдельные state(состояния) в классе
# StatesGroup - используется для определения состояний внутри машинах состояний (переменных)
class Form(StatesGroup):
# то что вводишь на дайвинчике
    name = State()
    age = State()
    sex = State()
    about = State()
    photo = State()