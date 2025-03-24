import telebot
import os
import logging
import time

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота с токеном из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# ID канала (для публичного канала используйте @username, для приватного — числовой chat_id)
CHANNEL_ID = "@kalkopred"  # Убедитесь, что это правильный ID

# Функция проверки подписки
def check_subscription(user_id):
    try:
        # Проверяем статус пользователя в канале
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        logger.info(f"Статус пользователя {user_id} в канале {CHANNEL_ID}: {member.status}")
        if member.status in ["member", "administrator", "creator"]:
            return True
        else:
            return False
    except telebot.apihelper.ApiTelegramException as e:
        if "chat not found" in str(e).lower():
            logger.error(f"Канал {CHANNEL_ID} не найден. Проверьте правильность CHANNEL_ID.")
        elif "bot is not a member" in str(e).lower():
            logger.error(f"Бот не является участником канала {CHANNEL_ID}. Добавьте бота как администратора.")
        elif "not enough rights" in str(e).lower():
            logger.error(f"У бота недостаточно прав для проверки участников в канале {CHANNEL_ID}. Дайте боту права администратора.")
        else:
            logger.error(f"Ошибка при проверке подписки: {e}")
        return False
    except Exception as e:
        logger.error(f"Неизвестная ошибка при проверке подписки: {e}")
        return False

# Команда для получения chat_id (для отладки, если канал приватный)
@bot.message_handler(commands=['getchatid'])
def get_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"Chat ID этого чата: {chat_id}")
    logger.info(f"Пользователь {message.from_user.id} запросил chat_id: {chat_id}")

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user = message.from_user

    # Проверка подписки
    if not check_subscription(user_id):
        bot.reply_to(message, f"Привет, {user.first_name}! Чтобы использовать бота, подпишись на канал: {CHANNEL_ID}")
        return

    welcome_message = f"Привет, {user.first_name}! Ты подписан на канал, и я готов помогать! 😄"
    bot.reply_to(message, welcome_message)
    logger.info(f"Отправлено приветствие пользователю {user.first_name} ({user.id})")

# Обработчик всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def echo(message):
    user_id = message.from_user.id
    user = message.from_user

    # Проверка подписки
    if not check_subscription(user_id):
        bot.reply_to(message, f"Чтобы использовать бота, подпишись на канал: {CHANNEL_ID}")
        return

    bot.reply_to(message, f"Вы сказали: {message.text}")
    logger.info(f"Получено сообщение от {user.first_name}: {message.text}")

# Запуск бота с polling
def main():
    logger.info("Бот запущен и работает...")
    while True:
        try:
            bot.polling(none_stop=True, interval=1)
        except Exception as e:
            logger.error(f"Ошибка при работе бота: {e}")
            time.sleep(5)  # Задержка перед перезапуском

if __name__ == "__main__":
    main()