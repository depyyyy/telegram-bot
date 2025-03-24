import telebot
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Инициализация бота с токеном из переменной окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    logger.error("BOT_TOKEN не найден в переменных окружения!")
    exit(1)

bot = telebot.TeleBot(BOT_TOKEN)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user = message.from_user
    welcome_message = f"Привет, {user.first_name}! Я твой бот, работающий 24/7! 😄"
    bot.reply_to(message, welcome_message)
    logger.info(f"Отправлено приветствие пользователю {user.first_name} ({user.id})")

# Обработчик всех текстовых сообщений
@bot.message_handler(content_types=['text'])
def echo(message):
    bot.reply_to(message, f"Вы сказали: {message.text}")
    logger.info(f"Получено сообщение от {user.first_name}: {message.text}")

# Запуск бота с polling
def main():
    logger.info("Бот запущен и работает...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка при работе бота: {e}")
        main()  # Перезапуск при ошибке

if __name__ == "__main__":
    main()