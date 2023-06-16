from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters
from telegram import Update
from tinydb import TinyDB, Query
import os

TOKEN = os.environ.get('TOKEN')

# Создаем или открываем базу данных
db = TinyDB('db.json', indent=4)
users = db.table('users')

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat.id

    # Проверяем, существует ли запись с заданным chat_id в базе данных
    if not users.contains(Query().user_id == chat_id):
        user = {
            "first_name": update.message.from_user.first_name,
            "last_name": update.message.from_user.last_name,
            "username": update.message.from_user.username,
            'user_id': chat_id
        }

        users.insert(user)
        context.bot.send_message(chat_id, 'Добро пожаловать наш бот!')
    else:
        context.bot.send_message(chat_id, 'С возвращением наш бот!')

def main():
    # Создаем экземпляр Updater и передаем токен
    updater = Updater(token=TOKEN)
    dp = updater.dispatcher

    # Добавляем обработчик команды /start
    dp.add_handler(CommandHandler(command='start', callback=start))

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
