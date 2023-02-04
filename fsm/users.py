import app_logger as logger
from aiogram.dispatcher.filters.state import State, StatesGroup


log = logger.get_logger(__name__)


class StateUser(StatesGroup):
    enter_id = State()
    enter_meets = State()
    enter_agent_reg = State()
    enter_agent_act = State()
    enter_UP = State()
    check_sales = State()
    change_sales = State()
    changed_sales = State()
