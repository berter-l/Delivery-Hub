`Delivery Hub API
О проекте
Delivery Hub API - это бэкенд-сервис для управления доставкой, разработанный на FastAPI.
Система обеспечивает взаимодействие между администраторами, курьерами и партнерами (ресторанами/магазинами) 
для эффективной обработки заказов.
`



# **Функционал**

# Администратор
1. Авторизация администраторов
2. Просмотр и фильтрация заказов
3. Управление партнерами (подтверждение регистрации)
4. Управление курьерами (подтверждение регистрации)

# Курьер

1. Регистрация и авторизация
2. Просмотр доступных заказов
3. Принятие заказов
4. Обновление статуса заказа (pickup, deliver, cancel)
5. Просмотр активных и завершенных заказов

# Партнер

1. Регистрация и авторизация (API-ключ)
2. Управление заказами (создание, просмотр, удаление)
3. Обновление профиля

## Стек технологий

* FastAPI - веб-фреймворк
* SQLAlchemy - ORM
* PostgreSQL - база данных
* Alembic - миграции
* Docker и Docker Compose - контейнеризация
* Nginx - веб-сервер

# Запуск проекта

## Требования
1. Docker и Docker Compose
2. Установка и запуск
3. Клонируйте репозиторий:
4. git clone <repository-url>
5. cd delivery-hub
6. Запустите приложение с помощью Docker Compose:
7. docker-compose up -d

Приложение будет доступно по адресу:
http://localhost:8000

Документация API доступна по адресу:
http://localhost:8000/docs

## API Endpoints

# Администратор

* POST /api/v1/admin/login - Вход администратора
* GET /api/v1/admin/orders - Получение заказов с фильтрацией
* GET /api/v1/partners - Получение неподтвержденных партнеров
* POST /api/v1/admin/partners/{partner_id}/approve - Подтверждение партнера
* GET /api/v1/admin/couriers - Получение курьеров
* POST /api/v1/admin/couriers/{courier_id}/approve - Подтверждение курьера

# Курьер
* POST /api/v1/couriers/register - Регистрация курьера
* POST /api/v1/couriers/login - Вход курьера
* GET /api/v1/couriers/me - Профиль курьера
* POST /api/v1/couriers/logout - Выход
* GET /api/v1/orders/courier/pending - Доступные заказы
* POST /api/v1/orders/courier/{order_id}/accept - Принять заказ
* PATCH /api/v1/orders/courier/{order_id}/pickup - Забрать заказ
* PATCH /api/v1/orders/courier/{order_id}/deliver - Доставить заказ
* PATCH /api/v1/orders/courier/{order_id}/cancel - Отменить заказ
* GET /api/v1/orders/courier/me - Активные заказы
* GET /api/v1/orders/courier - История заказов

# Партнер
* POST /api/v1/partners/register - Регистрация партнера
* POST /api/v1/partners/login - Вход партнера
* PATCH /api/v1/partners/me - Обновление профиля
* POST /api/v1/orders/partner - Создание заказа
* GET /api/v1/orders/partner - Заказы партнера
* DELETE /api/v1/orders/partner/{order_id} - Удаление заказа

