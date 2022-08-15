import pytz

from django.db import models


STATUS_CHOISES = (("NONE", "none"), ("SUCCESS", "success"), ("FAIL", "fail"))
time = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class OperatorCode(models.Model):
    operator_code = models.CharField(max_length=3, verbose_name="Код мобильного оператора")

    def __str__(self):
        return str(self.operator_code)


class Tag(models.Model):
    tag = models.CharField(max_length=50, verbose_name="Произвольная метка")

    def __str__(self):
        return self.tag


class MailList(models.Model):
    date_of_start = models.DateTimeField(null=False, verbose_name="Дата и время запуска рассылки")
    text_message = models.TextField(null=False, verbose_name="Текст сообщения для доставки клиенту")
    filter_tag = models.ForeignKey(
        Tag,
        null=False,
        on_delete=models.CASCADE,
        verbose_name="Фильтрация свойств клиента по произвольной метке",
    )
    filter_operator_code = models.ForeignKey(
        OperatorCode,
        null=False,
        on_delete=models.ForeignKey,
        verbose_name="Фильтрация свойств клиента по мобильному оператору",
    )
    date_of_ending = models.DateTimeField(
        null=False, verbose_name="Дата и время окончания рассылки"
    )

    @property
    def messages(self):
        return Message.objects.filter(mail_list_id=self.id)

    def __str__(self):
        return f"Рассылка: {self.id} - {self.date_of_start}"


class Client(models.Model):
    phone_number = models.CharField(
        max_length=11,
        null=False,
        verbose_name="Номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)",
    )
    operator_code = models.ForeignKey(
        OperatorCode, null=False, on_delete=models.CASCADE, verbose_name="Код мобильного оператора"
    )
    tag = models.ForeignKey(
        Tag, null=False, on_delete=models.CASCADE, verbose_name="Произвольная метка"
    )
    timezone = models.CharField(
        max_length=32, choices=time, default="Europe/Moscow", verbose_name="Часовой пояс"
    )

    def __str__(self):
        return f"Клиент: {self.id } - {self.phone_number}"


class Message(models.Model):
    start_of_send = models.DateTimeField(
        null=False, auto_now_add=True, verbose_name="Дата и время создания отправки"
    )
    status_of_send = models.CharField(
        null=False,
        max_length=8,
        choices=STATUS_CHOISES,
        default="NONE",
        verbose_name="Статус отправки",
    )
    mail_list_id = models.ForeignKey(
        MailList, null=False, on_delete=models.CASCADE, verbose_name="ID рассылки"
    )
    client_id = models.ForeignKey(
        Client, null=False, on_delete=models.CASCADE, verbose_name="ID клиента"
    )

    def __str__(self):
        return f"Сообщение: {self.id} - {self.mail_list_id} для {self.status_of_send}"


class MailListStat(models.Model):
    mail_list_id = models.IntegerField()
    success = models.IntegerField()
    fail = models.IntegerField()
    none = models.IntegerField()

    class Meta:
        managed = False

    @staticmethod
    def get_stat_by_id(mail_list_id):
        success_status = Message.objects.filter(
            mail_list_id=mail_list_id, status_of_send="SUCCESS"
        ).count()
        fail_status = Message.objects.filter(
            mail_list_id=mail_list_id, status_of_send="FAIL"
        ).count()
        none_status = Message.objects.filter(
            mail_list_id=mail_list_id, status_of_send="NONE"
        ).count()
        return dict(
            mail_list_id=mail_list_id,
            success=success_status,
            fail=fail_status,
            none=none_status,
        )
