import json
import time

import requests
from django.db.models import Q

from fabrique_notification_service.celery import app
from fabrique_notification_service.settings import PROBE_SERVER_URL, PROBE_SERVER_TOKEN
from mailing_list.models import MailList, Client, Message


@app.task
def maillist_task(mail_list_id):
    mail_list = MailList.objects.get(id=mail_list_id)
    operator_code = mail_list.operator_code
    tag = mail_list.tag
    clients = Client.objects.filter(Q(operator_code__exact=operator_code) & Q(tag__exact=tag))
    for client in clients:
        message = Message(status_of_send="NONE", mail_list_id=mail_list_id, client_id=client)
        message.save()
        message_id = message.id
        phone_number = message.client_id.phone_number
        text_message = mail_list.text
        message_task.delay(message_id, phone_number, text_message)


@app.task
def message_task(message_id, phone_number, text_message):
    url = "{}/send/{}".format(PROBE_SERVER_URL, message_id)
    data = {
        "message_id": message_id,
        "phone_number": phone_number,
        "text_message": text_message,
    }
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer {}".format(PROBE_SERVER_TOKEN),
        "Content-Type": "application/json",
    }

    counter = 0
    while counter < 3:
        response = requests.post(url=url, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            message = Message.objects.get(id=message_id)
            message.status_of_send = "SUCCESS"
            message.save()
            return True
        else:
            counter += 1
            time.sleep(300)
    message = Message.objects.get(id=message_id)
    message.status_of_send = "FAIL"
    message.save()
    return True
