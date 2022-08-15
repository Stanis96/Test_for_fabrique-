
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

### Документация OpenAPI
    127.0.0.1:8000/docs/
    

