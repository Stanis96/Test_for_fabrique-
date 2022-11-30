
  <h3 align="center">Тестовое задание: "Сервис управления рассылками API администрирования и получения статистики"
 от Фабрики Решений</h3>

### Используемый стек технологий в проекте:
* Django
* Django REST framework
* Celery
* Redis
* Poetry
* Swagger
* SQLite3

### Перед запуском выполните:

* Виртуальное окружение:
  ```sh
  poetry config virtualenvs.in-project true
  poetry install
  ```
* В корне проекта создайте ```.env``` и задайте значения переменных:
    ```sh
    DJANGO_SECRET_KEY=
    PROBE_SERVER_TOKEN=
    DEBUG=
    CELERY_BROKER_URL=
    CELERY_RESULT_BACKEND=
    PROBE_SERVER_URL=
    ```
* Cоздание и применение миграции:
    ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```

### Документация OpenAPI:
    127.0.0.1:8000/docs/

### Условие задания:
Спроектировать и разработать сервис, который по заданным правилам запускает рассылку по списку клиентов.
Сущность "рассылка" имеет атрибуты:

•уникальный id рассылки
•дата и время запуска рассылки
•текст сообщения для доставки клиенту
•фильтр свойств клиентов, на которых должна быть произведена рассылка (код мобильного оператора, тег)
•дата и время окончания рассылки: если по каким-то причинам не успели разослать все сообщения - никакие сообщения клиентам после этого времени доставляться не должны

Сущность "клиент" имеет атрибуты:
•уникальный id клиента
•номер телефона клиента в формате 7XXXXXXXXXX (X - цифра от 0 до 9)
•код мобильного оператора
•тег (произвольная метка)
часовой пояс

Сущность "сообщение" имеет атрибуты:
* уникальный id сообщения
* дата и время создания (отправки)
* статус отправки
* id рассылки, в рамках которой было отправлено сообщение
* id клиента, которому отправили

Спроектировать и реализовать API для:
•добавления нового клиента в справочник со всеми его атрибутами
•обновления данных атрибутов клиента
•удаления клиента из справочника
•добавления новой рассылки со всеми её атрибутами
•получения общей статистики по созданным рассылкам и количеству отправленных сообщений по ним с группировкой по статусам
•получения детальной статистики отправленных сообщений по конкретной рассылке
•обновления атрибутов рассылки
•удаления рассылки
•обработки активных рассылок и отправки сообщений клиентам

Логика рассылки
•После создания новой рассылки, если текущее время больше времени начала и меньше времени окончания - должны быть выбраны из справочника все клиенты, которые подходят под значения фильтра, указанного в этой рассылке и запущена отправка для всех этих клиентов.
•Если создаётся рассылка с временем старта в будущем - отправка должна стартовать автоматически по наступлению этого времени без дополнительных действий со стороны пользователя системы.
•По ходу отправки сообщений должна собираться статистика (см. описание сущности "сообщение" выше) по каждому сообщению для последующего формирования отчётов.
•Внешний сервис, который принимает отправляемые сообщения, может долго обрабатывать запрос, отвечать некорректными данными, на какое-то время вообще не принимать запросы. Необходимо реализовать корректную обработку подобных ошибок. Проблемы с внешним сервисом не должны влиять на стабильность работы разрабатываемого сервиса рассылок.

API внешнего сервиса отправки
Для интеграции с разрабатываемым проектом в данном задании существует внешний сервис, который может принимать запросы на отправку сообщений в сторону клиентов.
OpenAPI спецификация находится по адресу: https://probe.fbrq.cloud/docs
В этом API предполагается аутентификация с использованием JWT. Токен доступа предоставлен вам вместе с тестовым заданием.
