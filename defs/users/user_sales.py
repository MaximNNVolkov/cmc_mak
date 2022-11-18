import app_logger as loger
from aiogram.utils import markdown as fmt
from defs.classes import User, UserSales
from fsm import StateUser
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from .checks import CheckMsg
from keyboards import inline


log = loger.get_logger(__name__)


def txt_false():
    return 'Вводи только цифры. Давай снова'


def txt_total(u: User, d: dict):
    sales = ''
    d_total = UserSales()
    for k in d_total.my_d.keys():
        sales = ' '.join([sales, d_total.my_d[k], d[k], '\n'])
    text = fmt.text(
        fmt.text(u.get_url(), ', ', sep=''),
        fmt.text('Вот что получилось:'),
        fmt.text(sales),
        sep='\n')
    return text


async def msg_process(msg: Message, state: FSMContext, key: str):
    d = await state.get_data()
    res = CheckMsg.CheckNum(msg.text)
    if res:
        d[key] = msg.text
        await state.set_data(data=d)
        await msg.answer(text='Отлично.')
    else:
        await msg.answer(text=txt_false())
    return res


async def sales_start(msg: Message, state: FSMContext):
    u = User(msg.from_user)
    u.add_user()
    log.info(u.info_user())
    await state.set_state(StateUser.enter_id)
    await msg.answer(text=fmt.text(
            fmt.text(u.get_url(), ', ', sep=''),
            fmt.text('Введите Ваш id'),
            sep=''))


async def enter_id(msg: Message, state: FSMContext):
    u = User(msg.from_user)
    log.info(' '.join([await state.get_state(), msg.text, u.info_user()]))
    if await msg_process(msg, state, 'id'):
        await state.set_state(StateUser.enter_bch)
        await msg.answer(text='Введите БЧ.')


async def enter_bch(msg: Message, state: FSMContext):
    u = User(msg.from_user)
    log.info(' '.join([await state.get_state(), msg.text, u.info_user()]))
    if await msg_process(msg, state, 'bch'):
        await state.set_state(StateUser.enter_sup)
        await msg.answer(text='Введите СУП.')


async def enter_sup(msg: Message, state: FSMContext):
    u = User(msg.from_user)
    log.info(' '.join([await state.get_state(), msg.text, u.info_user()]))
    if await msg_process(msg, state, 'sup'):
        await state.set_state(StateUser.enter_szdor)
        await msg.answer(text='Введите СберЗдоровье.')


async def enter_szdor(msg: Message, state: FSMContext):
    u = User(msg.from_user)
    log.info(' '.join([await state.get_state(), msg.text, u.info_user()]))
    if await msg_process(msg, state, 'szdor'):
        await state.set_state(StateUser.check_sales)
        await msg.answer(text=txt_total(u, await state.get_data()),
                         reply_markup=inline.UsersCheckSales.create_kb())


async def check_sales_ok(cb: CallbackQuery, state: FSMContext):
    u = User(cb.from_user)
    log.info(' '.join([await state.get_state(), cb.data, u.info_user()]))
    us = UserSales()
    res = us.save_result(u.id, await state.get_data())
    if res == True:
        await state.reset_state()
        await cb.message.answer(text='Отправлено.')
    else:
        await cb.message.answer(text=txt_total(u, await state.get_data()),
                                reply_markup=inline.UsersCheckSales.create_kb())


async def check_sales_false(cb: CallbackQuery, state: FSMContext):
    u = User(cb.from_user)
    log.info(' '.join([await state.get_state(), cb.data, u.info_user()]))
    await state.set_state(StateUser.change_sales)
    kb = inline.UserProducts()
    await cb.message.answer(text='Что исправить?',
                            reply_markup=kb.create_kb())


async def change_values(cb: CallbackQuery, state: FSMContext):
    u = User(cb.from_user)
    log.info(' '.join([await state.get_state(), cb.data, u.info_user()]))
    d = UserSales()
    await cb.message.answer(text=fmt.text(
        fmt.text('Введите правильное значение '),
        fmt.text(d.my_d[cb.data.split(':')[-1]]),
        fmt.text('.'), sep=''
    ))
    d = await state.get_data()
    d['change'] = cb.data.split(':')[-1]
    await state.set_data(data=d)
    await state.set_state(StateUser.changed_sales)


async def changed_value(msg: Message, state: FSMContext):
    u = User(msg.from_user)
    log.info(' '.join([await state.get_state(), msg.text, u.info_user()]))
    d = await state.get_data()
    if await msg_process(msg, state, d['change']):
        await state.set_state(StateUser.check_sales)
        await msg.answer(text=txt_total(u, await state.get_data()),
                         reply_markup=inline.UsersCheckSales.create_kb())
