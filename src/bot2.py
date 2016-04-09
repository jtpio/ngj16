import os
import asyncio
import logging
import sys
import telepot
import time
from telepot.async.delegate import per_chat_id, create_open
from StateMachineManager import StateMachineManager

TELEGRAM_BOT_TOKEN_KRKKRK = os.getenv('TELEGRAM_BOT_TOKEN_KRKKRK', '')

DIRNAME = os.path.dirname(__file__)
RES_DIR = os.path.join(DIRNAME, '../res/')
STATES_JSON = os.path.join(DIRNAME, '../res/data/planet.json')

# Enable logging
logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)

logger = logging.getLogger(__name__)


class PlayerHandler(telepot.async.helper.ChatHandler):

    def __init__(self, seed_tuple, timeout):
        super(PlayerHandler, self).__init__(seed_tuple, timeout)
        self._count = 0
        self.state_machine = StateMachineManager(STATES_JSON, "landing")

    def _start_bot(self):
        self.state_machine.reset()

    @asyncio.coroutine
    def handle_metadata(self, chat_id, metadata):
        keyboard = {'hide_keyboard': True}
        for metadata_item in metadata:
            item_type = metadata_item['type']
            item_data = metadata_item['data']
            yield from self.sender.sendChatAction('typing')
            if item_type == 'text':
                yield from self.sender.sendMessage(
                    item_data,
                    reply_markup=keyboard
                )
            if item_type == 'img':
                yield from self.sender.sendPhoto(
                    open(RES_DIR + item_data, 'rb'),
                    reply_markup=keyboard
                )
            if item_type == 'snd':
                yield from self.sender.sendVoice(
                    open(RES_DIR + item_data, 'rb'),
                    reply_markup=keyboard
                )
            if item_type == 'delay':
                yield from asyncio.sleep(int(item_data))


    @asyncio.coroutine
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if content_type == 'text':
            keyboard = {'hide_keyboard': True}
            text = msg['text']
            # commands
            action = text
            if text == '/start':
                self._start_bot()
                action = 'go'
            elif text == '/help':
                yield from self.sender.sendMessage(
                    'Help? You need help? I am the one needing help!'
                )
                return

            res = self.state_machine.send_message(action)
            triggers = res['triggers']
            metadata = res['metadata']

            if len(metadata) == 0:
                return

            yield from self.handle_metadata(chat_id, res['metadata'])

            if len(triggers) > 0:
                keyboard = {'keyboard': [triggers]}

            yield from self.sender.sendMessage(
                'So what should I do?',
                reply_markup=keyboard
            )

    # TODO: handle errors



def main():
    bot = telepot.async.DelegatorBot(TELEGRAM_BOT_TOKEN_KRKKRK, [
        (per_chat_id(), create_open(PlayerHandler, timeout=None))
    ])

    loop = asyncio.get_event_loop()
    loop.create_task(bot.messageLoop())
    print('Bot is listening')

    loop.run_forever()


if __name__ == '__main__':
    main()
