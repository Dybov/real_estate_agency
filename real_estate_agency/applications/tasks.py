from .views import TelegramBot, MSG_RECEIVERS

from real_estate_agency.celery import app

@app.task
def lols(msg):
    for r in MSG_RECEIVERS:
        TelegramBot.sendMessage(r, msg)