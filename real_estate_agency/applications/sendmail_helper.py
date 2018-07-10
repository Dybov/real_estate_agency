from django.core.mail import mail_managers
# from django.

# It will use celery in the future
def sendApplicationToTheManagers(title, message):
    mail_managers(title, '', html_message=message.replace('\n','<br/>'))
