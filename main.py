import asyncio, logging
import sqlite3 as sq
from aiogram import Dispatcher, Bot
from config.config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from commands import router as cmdrouter


async def main():
    storage = MemoryStorage()  # Создаем хранилище

    bot = Bot(config.BOT_TOKEN.get_secret_value())  # Получаем токен бота из файла с конфигом
    dp = Dispatcher(storage=storage)  # Создаем диспетчер и передаем ему храналище
    dp.include_routers(cmdrouter)  # Добавляем роутеры в диспетчер
    logging.basicConfig(filename='logs/logs.log', level=logging.DEBUG)  # Указываем файл для логирования

    with sq.connect('bot.db') as con:  # Создаем в БД таблицу с колонками id, user_name и iq
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id TEXT,
        iq INTEGER NOT NULL DEFAULT 0,
        call_time INTEGER NOT NULL DEFAULT 0)""")

    logging.info('bot is starting')

    await bot.delete_webhook(drop_pending_updates=True)  # Игнорируем все команды, отправленные до запуска бота
    await dp.start_polling(bot)  # Запуск бота


if __name__ == '__main__':
    asyncio.run(main())
