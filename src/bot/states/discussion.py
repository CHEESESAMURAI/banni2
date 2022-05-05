from aiogram.dispatcher.filters.state import StatesGroup, State


class AppendDiscussion(StatesGroup):
    sending = State()
