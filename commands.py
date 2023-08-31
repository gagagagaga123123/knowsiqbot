from aiogram import types, Router
from aiogram.filters import Command
from random import  randint
import sqlite3 as sq
from messages import HELP_MESSAGE, START_MESSAGE
from keyboards import load_start_kb, load_default_buttons
from time import time
from middlewares import RegistrationCheckMiddleware
import logging

router = Router()

router.message.middleware(RegistrationCheckMiddleware())

@router.message(Command('start'))  # Обработка команды /start
async def start_cmd(message: types.Message):
    await message.answer(START_MESSAGE,reply_markup=load_start_kb())
    logging.info('start command')

@router.message(Command('register'),flags = {"reg" : "mustnotberegistered"})  # Обработка команды /register
async def reg_cmd(message:types.Message):
    with (sq.connect('bot.db') as con):
        logging.info('connected to database')
        cur = con.cursor()
        
        future_id = cur.execute("""SELECT COUNT(*) FROM user""").fetchone()[0]  # Создаем id пользователя с помощью кол-ва участников
        tg = message.from_user.id  # Берем telegram id пользователя

        cur.execute(f"""INSERT INTO user VALUES({future_id},{tg},0,0)""")  # Добавляем строчку в таблицу

        await message.answer('Вы были успешно зарегестрированы в системе!',reply_markup=load_default_buttons())
        logging.info('registered in database, disconnected from database')

@router.message(Command('iq'),flags = {"reg" : "mustberegistered"})  # Обработка команды /iq (Вывод IQ пользователя в чат)
async def get_iq_cmd(message: types.Message):
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        logging.info('connected to database')

        cur.execute(f"""SELECT iq FROM user WHERE telegram_id == {str(message.from_user.id)}""")  # Ищем IQ юзера через его tg id
        iq = cur.fetchone()[0]

        await message.answer(f'Ваш IQ равен {iq}',reply_markup=load_default_buttons())
        logging.info('iq command, disconnected from database')


@router.message(Command('changeiq'),flags = {"changeiq" : "changeiq","reg" : "mustberegistered"})
async def change_iq_cmd(message: types.Message):  # Рандомно увеличит/уменьшит iq пользователя
    with sq.connect('bot.db') as con:
        cur = con.cursor()
        logging.info('connected to database')

        cur.execute(f"""SELECT iq FROM user WHERE telegram_id == {str(message.from_user.id)}""")  # Берем iq юзера
        iq = cur.fetchone()[0]

        changediq = iq + randint(-10,10)

        cur.execute(f"""UPDATE user SET iq = {changediq}, call_time = {time()} WHERE telegram_id == {str(message.from_user.id)}""")

        await message.answer(iq_changes_message(changediq,iq),reply_markup=load_default_buttons())
        logging.info('changeiq command, disconnected from database')



def iq_changes_message(changediq,iq) -> str:
    if changediq == iq:
        answer = 'Ваш IQ не изменился!'
    elif changediq > iq:
        answer = f'Поздравляем! Ваш iq вырос на {changediq - iq}'
    elif changediq < iq:
        answer = f'К сожалению, Ваш iq уменьшился на {iq - changediq}'

    return answer





@router.message(Command('help'))  # Обработка команды help
async def help_cmd(message: types.Message):
    await message.reply(HELP_MESSAGE) # HELP_MESSAGE в keyboards.py

