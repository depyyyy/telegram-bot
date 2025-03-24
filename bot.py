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

# ID вашего канала (замените на реальный chat_id канала t.me/kalkopred)
CHANNEL_ID = "@kalkopred"  # Укажите ID канала в формате @username

# Функция проверки подписки
def check_subscription(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except Exception as e:
        logger.error(f"Ошибка при проверке подписки: {e}")
        return False

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