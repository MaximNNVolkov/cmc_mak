from fsm import StateUser
from aiogram import Dispatcher
from defs import enter_id, enter_bch, enter_sup, enter_szdor, check_sales_ok,\
    change_values, changed_value, check_sales_false
from keyboards.inline import UserProducts

d = UserProducts()

def register_user(dp: Dispatcher):
    dp.register_message_handler(enter_id, state=StateUser.enter_id)
    dp.register_message_handler(enter_bch, state=StateUser.enter_bch)
    dp.register_message_handler(enter_sup, state=StateUser.enter_sup)
    dp.register_message_handler(enter_szdor, state=StateUser.enter_szdor)
    dp.register_callback_query_handler(check_sales_ok, text='CheckOk', state=StateUser.check_sales)
    dp.register_callback_query_handler(check_sales_false, text='CheckChange', state=StateUser.check_sales)
    dp.register_callback_query_handler(change_values, d.cb.filter(), state=StateUser.change_sales)
    dp.register_message_handler(changed_value, state=StateUser.changed_sales)
