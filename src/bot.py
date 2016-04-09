import os
import logging
import telegram
from telegram.ext import Updater
import time
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


stateMachineManager = StateMachineManager(STATES_JSON, "landing")


def start(bot, update):
    stateMachineManager.reset()
    chat_id = update.message.chat_id
    res = stateMachineManager.send_message('go')
    handle_metadata(bot, chat_id, res['metadata'])
    custom_keyboard = [res['triggers']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    bot.sendMessage(
        chat_id,
        text='So what should I do?',
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
        bot.sendChatAction(
            chat_id=chat_id,
            action=telegram.ChatAction.TYPING
        )
        if item_type == 'text':
            bot.sendMessage(
                chat_id,
                text=item_data,
                reply_markup=telegram.ReplyKeyboardHide()
            )
        if item_type == 'img':
            bot.sendPhoto(
                chat_id,
                photo=open(RES_DIR + item_data, 'rb')
            )
        if item_type == 'snd':
            bot.sendVoice(
                chat_id,
                voice=open(RES_DIR + item_data, 'rb')
            )
        if item_type == 'delay':
            time.sleep(int(item_data))


def handle_message(bot, update):
    chat_id = update.message.chat_id
    text = update.message.text
    res = stateMachineManager.send_message(text)
    print("TEXT:", text)
    handle_metadata(bot, chat_id, res['metadata'])
    triggers = res['triggers']
    if len(triggers) > 0:
        custom_keyboard = [triggers]
        reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    else:
        reply_markup = telegram.ReplyKeyboardHide()

    bot.sendMessage(
        chat_id,
        text='So what should I do?',
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
