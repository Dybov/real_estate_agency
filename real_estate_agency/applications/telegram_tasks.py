import requests
import os
import urllib3
from urllib3.exceptions import MaxRetryError
import time

from django.conf import settings

from real_estate_agency.celery import app

from celery import group

from telepot import Bot as TBot
from telepot.exception import TelegramError
from telepot.api import set_proxy

_default_pool_params = dict(num_pools=3, maxsize=10, retries=1, timeout=30)
_onetime_pool_params = dict(num_pools=1, maxsize=1, retries=1, timeout=30)
_pools = {
    'default': urllib3.PoolManager(**_default_pool_params),
}
_onetime_pool_spec = (urllib3.PoolManager, _onetime_pool_params)

TOKEN = settings.TELEGRAM_TOKEN


def serverIsReachable(hostname, protocol='https://'):
    """
    Check if server is reachable

    """
    response = os.system("ping -c 1 " + hostname)
    return response == 0


def requestProxies(number=10):
    proxy_list = getProxiesFrom_pubproxy(number)
    if not proxy_list:
        proxy_list = getProxiesFrom_getproxylist(number)
    return proxy_list


def getProxiesFrom_pubproxy(number=10):
    """
    Get dynamic proxies list from http://pubproxy.com/api/proxy

    """
    params = {
        'country': 'US,CA',
        'type': 'http',
        'https': 'true',
        'speed': 9,
        'limit': number,
    }
    url = "http://pubproxy.com/api/proxy"
    result = requests.get(url, params=params)
    if result.ok is True:
        try:
            return result.json().get('data', [])
        except ValueError:
            pass
    return []


def getProxiesFrom_getproxylist(number):
    params = {
        'country': ['US', 'CA'],
        'protocol': 'http',
        'allowsHttps': 1,
        'minDownloadSpeed': 9,
    }
    url = 'https://api.getproxylist.com/proxy'
    out = []
    for i in range(number):
        result = requests.get(url, params=params)
        if result.ok is True:
            try:
                res = result.json()
                res['type'] = res.get('protocol', 'http')
                res['ipPort'] = '%s:%s' % (res.get('ip'), res.get('port'))
                out.append(result.json())
            except ValueError:
                pass
    return out


def resetTelegramServer():
    """
    Set reachable proxy for telebot from dynamic proxy list
    returns setted proxy or False

    """
    proxies = requestProxies()
    for _dict in proxies:
        ip = _dict.get('ip')
        if serverIsReachable(ip):
            proxy = '{protocol}://{ip_port}'.format(
                protocol=_dict.get('type'),
                ip_port=_dict.get('ipPort'),
            )
            user = _dict.get('user')
            password = _dict.get('password')
            if user or password:
                auth = (user, password)
            else:
                auth = None

            set_proxy(proxy, auth)
            return proxy
    return False


@app.task(bind=True, ignore_result=True)
def sendTelegramMessage(self, bot_token, chat_id, message, **kwargs):
    try:
        bot = TBot(bot_token)
        return bot.sendMessage(chat_id, message, parse_mode="html", **kwargs)
    except TelegramError:
        import logging
        # Get an instance of a logger
        logger = logging.getLogger(__name__)
        logger.critical('Bad telegram token is set %s' % TOKEN)
    except MaxRetryError as exc:
        res = resetTelegramServer()
        countdown = 10 * 60
        if res:
            countdown = 5
        self.retry(countdown=countdown, exc=exc)
    except Exception as exc:
        countdown = 15 * 60
        self.retry(countdown=countdown, exc=exc)


def sendStandartTelegramMessage(chat_id, message, **kwargs):
    return sendTelegramMessage.delay(TOKEN, chat_id, message, **kwargs)


@app.task
def sendTelegramMassMessages(receivers, msg, **kwargs):
    res = group(
        sendTelegramMessage.s(
            TOKEN,
            receiver,
            msg,
            **kwargs
        ) for receiver in receivers
    )()
    while not res.ready():
        time.sleep(5)
    return res.successful()


def sendTelegramMessageToTheAdmins(msg, **kwargs):
    receivers = settings.TELEGRAM_ADMINS_CHATS
    sendTelegramMassMessages.delay(receivers, msg, **kwargs)


def sendTelegramMessageToTheStaff(msg, **kwargs):
    receivers = settings.TELEGRAM_CHATS
    sendTelegramMassMessages.delay(receivers, msg, **kwargs)
