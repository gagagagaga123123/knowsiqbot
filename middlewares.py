from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message
import sqlite3 as sq
from time import time
from aiogram.dispatcher.flags import get_flag
from keyboards import load_start_kb, load_default_buttons
import logging


class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        logging.info('middleware started')

        changeiq = get_flag(data,'changeiq')
        reg = get_flag(data,'reg')

        if not reg:  # Если нет флага reg, то скипаем middleware и просто обрабатываем апдейт
            logging.info('middleware finished: no flags')
            return await handler(event, data)

        with sq.connect('bot.db') as con:
            logging.info('connected to database')
            cur = con.cursor()


            if reg:   # Если есть флаг reg, то проверяем его содержимое (у /register и (/iq и /changeiq) отличается)
                if reg == 'mustberegistered' and (all(str(event.from_user.id) != id[0] for id in cur.execute("""SELECT telegram_id FROM user""").fetchall())): # Проверка на то, зарегестрирован ли юзер
                    await event.answer('Вы еще не зарегестрированы в системе. Для регистрации введите /register',reply_markup=load_start_kb())
                    logging.error('user must be registered for this command, disconnected from database, middleware finished')
                    return
                elif reg == 'mustnotberegistered' and (cur.execute("""SELECT telegram_id FROM user""").fetchone() != None  # Проверка на то, не зарегестрирован ли уже пользователь
                                                      and any(str(event.from_user.id) == id[0] for id in cur.execute("""SELECT telegram_id FROM user""").fetchall())):
                    await event.answer('Вы уже зарегестрированы в системе',reply_markup=load_default_buttons())
                    logging.error('user must be not registered for this command, disconnected from database, middleware finished')
                    return
            if changeiq:  # Если /changeiq, то проверяем, прошло ли достаточно времени
                cur.execute(f"""SELECT call_time FROM user WHERE telegram_id == {str(event.from_user.id)}""")
                lasttime = cur.fetchone()[0]
                if time() - lasttime < 3600:  # lasttime - время предыдущего успешного запроса /changeiq в секундах
                    await event.answer('Доступно раз в час')
                    logging.error('not enough time left before previous change, disconnected from database, middleware finished')
                    return
            logging.info('disconnected from database')

            result = await handler(event, data)
            logging.info('middleware finished: no matches in flags')
            return result
