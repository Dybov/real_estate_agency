from django.core.mail import mail_managers
from real_estate_agency.celery import app


def sendMailToTheManagers(title, message):
    """ Wrapper for using it without delay in other parts of project """
    sendMailToTheManagersTask.delay(title, message)


@app.task(bind=True)
def sendMailToTheManagersTask(self, title, message):
    try:
        return mail_managers(
            title,
            '',
            html_message=message.replace('\n', '<br/>')
        )
    except Exception as exc:
        self.retry(countdown=30 * 60, exc=exc)
