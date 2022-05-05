from aiogram.dispatcher.filters.state import StatesGroup, State


class Mailing(StatesGroup):
    start_mailing = State()
    waiting_for_message = State()
