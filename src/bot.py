import os
import logging
import telegram
from telegram.ext import Updater
from StateMachineManager import StateMachineManager

TELEGRAM_BOT_TOKEN_KRKKRK = os.getenv('TELEGRAM_BOT_TOKEN_KRKKRK', '')
BOT_NAME = '@krkkrk_bot'

# DUMB
DIRNAME = os.path.dirname(__file__)
RES_DIR = os.path.join(DIRNAME, '../res/')
STATES_JSON = os.path.join(DIRNAME, '../res/data/planet.json')

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


stateMachineManager = StateMachineManager(STATES_JSON, "valley")


def start(bot, update):
    custom_keyboard = [stateMachineManager.get_current_display_texts()]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(
        update.message.chat_id,
        text='Hi!',
        reply_markup=reply_markup
    )


def help_message(bot, update):
    bot.sendMessage(
        update.message.chat_id,
        text='Help? You need help? I am the one needing help!'
    )


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def handle_metadata(bot, chat_id, metadata):
    for metadata_item in metadata:
        item_type = metadata_item['type']
        item_data = metadata_item['data']
        if item_type == 'text':
            bot.sendMessage(
                chat_id,
                text=item_data
            )
        if item_type == 'img':
            bot.sendPhoto(
                chat_id,
                photo=open(RES_DIR + item_data, 'rb')
            )


def handle_message(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    res = stateMachineManager.send_message(text)
    print("TEXT:", text)
    handle_metadata(bot, chat_id, res['metadata'])
    custom_keyboard = [res['triggers']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(
        chat_id,
        text=res['metadata'][0]["data"],
        reply_markup=reply_markup
    )


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN_KRKKRK)
    dp = updater.dispatcher
    dp.addTelegramCommandHandler('start', start)
    dp.addTelegramCommandHandler('help', help_message)

    dp.addTelegramMessageHandler(handle_message)

    dp.addErrorHandler(error)

    updater.start_polling()

    print('Bot is listening')

if __name__ == '__main__':
    main()
