from fsm import StateUser
from aiogram import Dispatcher
from defs import enter_id, enter_meets, enter_agent_reg, enter_agent_act, enter_UP, check_sales_ok,\
    change_values, changed_value, check_sales_false
from keyboards.inline import UserProducts

cb_change_prod = UserProducts()


def register_user(dp: Dispatcher):
    dp.register_message_handler(enter_id, state=StateUser.enter_id)
    dp.register_message_handler(enter_meets, state=StateUser.enter_meets)
    dp.register_message_handler(enter_agent_reg, state=StateUser.enter_agent_reg)
    dp.register_message_handler(enter_agent_act, state=StateUser.enter_agent_act)
    dp.register_message_handler(enter_UP, state=StateUser.enter_UP)
    dp.register_callback_query_handler(check_sales_ok, text='CheckOk', state=StateUser.check_sales)
    dp.register_callback_query_handler(check_sales_false, text='CheckChange', state=StateUser.check_sales)
    dp.register_callback_query_handler(change_values, cb_change_prod.cb.filter(), state=StateUser.change_sales)
    dp.register_message_handler(changed_value, state=StateUser.changed_sales)
