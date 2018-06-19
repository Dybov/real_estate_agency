import os
from urllib3.exceptions import MaxRetryError

from django.conf import settings

import telepot
from telepot.exception import TelegramError
from telepot.api import set_proxy


TOKEN = settings.TELEGRAM_TOKEN
TelegramBot = telepot.Bot(TOKEN)

MSG_RECEIVERS = settings.TELEGRAM_CHATS

TELEGRAM_PROXIES = settings.TELEGRAM_PROXIES

HOST = "t.me" # standart host


# Chech if server is reachable:
def serverIsReachable(hostname):
    response = os.system("ping -c 1 " + hostname)
    return response == 0


def resetServer():
    global HOST
    if not serverIsReachable(HOST):
        for protocol, ip, port, user, password in TELEGRAM_PROXIES:
            if serverIsReachable(ip):
                proxy = '{protocol}://{ip}:{port}'.format(
                    protocol=protocol, ip=ip, port=port,
                )
                if user or password:
                    auth = (user, password)
                else:
                    auth = None

                set_proxy(proxy, auth)
                
                HOST = ip
                return True


def sendTelegramMessage(bot, chat_id, message, **kwargs):
    try:
        bot.sendMessage(chat_id, message, parse_mode="html", **kwargs)
    except TelegramError:
        import logging
        # Get an instance of a logger
        logger = logging.getLogger(__name__)
        logger.critical('Bad telegram token is set %s' % TOKEN)
    except MaxRetryError:
        # For unreachable servers
        if resetServer():
            sendTelegramMessage(bot, chat_id, message, **kwargs)


def sendStandartTelegramMessage(chat_id, message, **kwargs):
    return sendTelegramMessage(TelegramBot, chat_id, message, **kwargs)


def sendTelegramMassMessages(receivers, msg, **kwargs):
    for receiver in receivers:
        sendStandartTelegramMessage(receiver, msg, **kwargs)


def sendTelegramMessageToTheAdmins(msg, **kwargs):
    receivers = settings.TELEGRAM_ADMINS_CHATS
    sendTelegramMassMessages(receivers, msg, **kwargs)


def sendTelegramMessageToTheStaff(msg, **kwargs):
    receivers = settings.TELEGRAM_CHATS
    sendTelegramMassMessages(receivers, msg, **kwargs)