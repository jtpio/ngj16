import os
import logging
from telegram.ext import Updater
from tempfile import NamedTemporaryFile
from gtts import gTTS

TELEGRAM_BOT_TOKEN_KRKKRK = os.getenv('TELEGRAM_BOT_TOKEN_KRKKRK', '')
BOT_NAME = '@krkkrk_bot'

# DUMB
DIRNAME = os.path.dirname(__file__)
TEST_GIF = open(os.path.join(DIRNAME, '../res/img/star.gif'), 'rb')
TEST_VID = open(os.path.join(DIRNAME, '../res/vid/slam_ball.mp4'), 'rb')

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text='Hi!')


def text_to_speech(bot, update):
    msg = update.message.text.replace(BOT_NAME, '')
    tts = gTTS(text=msg, lang='en')
    with NamedTemporaryFile() as fp:
        tts.write_to_fp(fp)
        # reopen the file so telegram can use it
        f = open(fp.name, 'rb')
        bot.sendVoice(
            chat_id=update.message.chat_id,
            voice=f,
            title='I can speak'
        )
        f.close()


def send_gif(bot, update):
    bot.sendDocument(
        chat_id=update.message.chat_id,
        document=TEST_GIF
    )


def send_video(bot, update):
    bot.sendVideo(
        chat_id=update.message.chat_id,
        video=TEST_VID
    )


def echo(bot, update):
    bot.sendMessage(update.message.chat_id, text=update.message.text)


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    updater = Updater(TELEGRAM_BOT_TOKEN_KRKKRK)

    dp = updater.dispatcher
    dp.addTelegramCommandHandler('start', start)
    dp.addTelegramCommandHandler('gif', send_gif)
    dp.addTelegramCommandHandler('video', send_video)

    dp.addTelegramMessageHandler(text_to_speech)

    dp.addErrorHandler(error)

    updater.start_polling()

    print('Bot is listening')

if __name__ == '__main__':
    main()
