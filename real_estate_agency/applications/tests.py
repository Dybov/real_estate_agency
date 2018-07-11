from unittest import skip

from django.test import TestCase, tag, override_settings
from django.conf import settings

from viberbot.api.messages import TextMessage

from .telegram_tasks import TOKEN, sendTelegramMessage
from .viber_tasks import VIBER_BOT, get_bot_admins, sendViberTextMessageToTheAdmins


@skip('Because Telegram is blocking in Russia with using web filters also. \
    So it is not reachable. Skip it until it will be unblocked')
@tag('telegram')
class TelegramBotTests(TestCase):
    @override_settings(CELERY_ALWAYS_EAGER=True)
    def setUp(self):
        self.TOKEN = TOKEN
        self.chat_id = settings.TELEGRAM_ADMINS_CHATS[0]

    @tag('delayed')
    def test_sendTelegramMessage(self):
        answer = sendTelegramMessage.delay(
            self.TOKEN,
            self.chat_id,
            "test_sendTelegramMessage is okay"
        )
        self.assertTrue(answer)


@tag('viber')
class ViberBotTests(TestCase):
    def setUp(self):
        self.bot = VIBER_BOT
        self.admins = settings.VIBER_BOT_TEST_ADMINS
        if not self.admins:
            self.admins = get_bot_admins()

    @tag('send')
    def test_sending_admin_message(self):
        # It will be delivered!
        msg = TextMessage(text="Run viber bot tests")
        for reciever in self.admins:
            answer = self.bot.send_messages(
                reciever,
                msg,
            )
            self.assertTrue(answer)

    def test_viber_valid_token(self):
        try:
            self.bot.get_account_info()
        except Exception:
            self.fail("Bot token is invalid!")
