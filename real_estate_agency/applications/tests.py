from django.test import TestCase, tag, override_settings
from django.conf import settings

from .telegram_tasks import TOKEN, sendTelegramMessage


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
