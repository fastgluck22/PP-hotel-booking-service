
## REST API cервис для управления номерами отеля и бронированиями, построенный на Django REST Framework, PostgreSQL и Docker

**Технологии:**
* Python 3.12
* Django & Django REST Framework
* PostgreSQL
* Poetry (управление зависимостями)
* Docker & Docker Compose

**Переменные окружения:**
Для конфигурации проекта создается файл `.env` на основе шаблона `.env.example`. 

- `SECRET_KEY` — секретный ключ приложения Django.
- `DEBUG` — режим отладки (`True` для разработки, `False` для продакшена).
- `ALLOWED_HOSTS` — список разрешенных хостов (например, `127.0.0.1,localhost`).
- `DB_NAME` — имя базы данных PostgreSQL.
- `DB_USER` — имя пользователя базы данных.
- `DB_PASSWORD` — пароль базы данных.
- `DB_HOST` — имя сервиса базы данных в Docker (по умолчанию `db`).
- `DB_PORT` — порт подключения к PostgreSQL (по умолчанию `5432`).

**Инструкция по запуску:**
1. Скопировать шаблон переменных окружения:
   `cp .env.example .env`
2. Собрать и запустить Docker-контейнеры в фоновом режиме:
   `docker compose up -d --build`
3. Применить миграции для создания структуры базы данных:
   `docker compose exec web python src/manage.py migrate`
4. Создать аккаунт администратора:
   `docker compose exec web python src/manage.py createsuperuser`

**Описание эндпоинтов:**
Базовый адрес сервиса: `http://127.0.0.1:8000/`
- `GET /admin/` — панель администратора Django.
- `GET /rooms/` — получение списка всех номеров.
- `POST /rooms/` — Добавление нового номера.
- `GET /rooms/<room_id>/` — детальная информация о конкретном номере.
- `PUT / PATCH / DELETE /rooms/<room_id>/` — редактирование или удаление номера.


- `GET /bookings/` — получение списка всех бронирований.
- `POST /bookings/` — создание нового бронирования.
- `GET /bookings/<booking_id>/` — детальная информация о конкретном бронировании.
- `PUT / PATCH / DELETE /bookings/<booking_id>/` — редактирование или удаление бронирования.

**Управление проектом:**
- просмотр логов веб-приложения: `docker compose logs -f web`
- остановка и удаление контейнеров: `docker compose down`