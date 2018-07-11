import re

from django.conf import settings

from real_estate_agency.celery import app

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import TextMessage


tag_regex = re.compile('<[^<>]+>')
bot_configuration = BotConfiguration(
    name=settings.VIBER_BOT_NAME,
    avatar=settings.VIBER_BOT_AVATAR,
    auth_token=settings.VIBER_BOT_TOKEN,
)

VIBER_BOT = Api(bot_configuration)


def getBotAdmins():
    if settings.DEBUG:
        return settings.VIBER_BOT_TEST_ADMINS or []
    members = VIBER_BOT.get_account_info()['members']
    admins = [member['id'] for member in members if member['role'] == 'admin']
    return admins


def removeTagsFromMessage(msg):
    return tag_regex.sub('', msg)


@app.task(bind=True)
def sendViberMessage(self, reciever, msg):
    try:
        if settings.DEBUG:
            msg += '\n\n[DEBUG MODE]'
        text_message = TextMessage(text=msg)
        return VIBER_BOT.send_messages(reciever, [text_message])
    except Exception as e:
        self.retry(countdown=60, exc=e)


def sendViberMassMessage(recievers, msg, remove_tags=True):
    if remove_tags is True:
        msg = removeTagsFromMessage(msg)

    responses = []
    for reciever in recievers:
        response = sendViberMessage.delay(reciever, msg)
        responses.append(response)
    return responses


def sendViberTextMessageToTheAdmins(msg, remove_tags=True):
    recievers = getBotAdmins()
    return sendViberMassMessage(recievers, msg, remove_tags=True)


def sendViberTextMessageToPrivateGroups(msg, remove_tags=True):
    recievers = settings.VIBER_BOT_PRIVATE_GROUPS
    return sendViberMassMessage(recievers, msg, remove_tags=True)
