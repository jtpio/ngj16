import os
import logging
import telegram
from telegram.ext import Updater
import StateMachine

TELEGRAM_BOT_TOKEN_KRKKRK = os.getenv('TELEGRAM_BOT_TOKEN_KRKKRK', '')
BOT_NAME = '@krkkrk_bot'

# DUMB
DIRNAME = os.path.dirname(__file__)
RES_DIR = os.path.join(DIRNAME, '../res/')

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def handle_message(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    res = StateMachine.send_message(text)
    custom_keyboard = [res['options']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(
        chat_id,
        text=res['text'],
        reply_markup=reply_markup
    )


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN_KRKKRK)

    dp = updater.dispatcher
    dp.addTelegramCommandHandler('start', start)

    dp.addTelegramMessageHandler(handle_message)

    dp.addErrorHandler(error)

    updater.start_polling()

    print('Bot is listening')

if __name__ == '__main__':
    main()
