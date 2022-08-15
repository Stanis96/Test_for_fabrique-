from django.db.models.signals import post_save
from django.dispatch import receiver
import pytz
from datetime import datetime

from mailing_list.models import MailList
from mailing_list.tasks import maillist_task


@receiver(post_save, mail_list=MailList)
def signal_maillist_task(mail_list, instance, **kwargs):
    now = datetime.utcnow().replace(tzinfo=pytz.utc)
    date_of_start = instance.date_of_start
    date_of_ending = instance.date_of_ending

    if (date_of_start <= now) and (date_of_ending > now):
        maillist_task.delay(instance.id)
    else:
        maillist_task.delay(instance.id, date_of_start=date_of_start)
    return True
