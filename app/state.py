from aiogram.fsm.state import StatesGroup, State



class Comment_for_day(StatesGroup):
    user_comment = State()


class Write_to_curator(StatesGroup):
    user_message = State()