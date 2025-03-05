# WareHouse
1. Начало работы

Перед использованием выполните:
python manage.py migrate  # Применить миграции
python manage.py createsuperuser  # Создать админа (опционально)

2. Регистрация пользователя

Эндпоинт: POST /users/

Пример запроса (HTTP):
POST /users/
Content-Type: application/json

{
    "username": "user1",
    "email": "user1@example.com",
    "password": "securepassword123",
    "user_type": "provider"  # или "consumer"
}
Ответ:
{
    "username": "user1",
    "email": "user1@example.com",
    "user_type": "provider"
}

3. Аутентификация

Эндпоинт: POST /api-token-auth/

Пример запроса:
POST /api-token-auth/
Content-Type: application/json

{
    "username": "user1",
    "password": "securepassword123"
}
Ответ:
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}

Используйте токен в заголовках:
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

4. Работа со складами

Эндпоинт: POST /warehouses/

Пример запроса:
POST /warehouses/
Content-Type: application/json
Authorization: Token YOUR_TOKEN

{
    "name": "Основной склад"
}

5. Работа с товарами

Эндпоинт: POST /products/

Пример запроса:
POST /products/
Content-Type: application/json
Authorization: Token YOUR_TOKEN

{
    "name": "Ноутбуки",
    "warehouse": 1,  # ID существующего склада
    "quantity": 0  # Начальное количество (опционально)
}

6. Операции с товаром

Эндпоинт: POST /transactions/

Для поставщика (user_type=provider):
POST /transactions/
Content-Type: application/json
Authorization: Token YOUR_TOKEN

{
    "product": 1,  # ID товара
    "transaction_type": "supply",
    "quantity": 50
}

Для потребителя (user_type=consumer):
POST /transactions/
Content-Type: application/json
Authorization: Token YOUR_TOKEN

{
    "product": 1,
    "transaction_type": "consume",
    "quantity": 10
}

Ответ (автоматически обновляет количество товара):
{
    "id": 1,
    "product": 1,
    "transaction_type": "supply",
    "quantity": 50,
    "created_at": "2023-10-05T12:34:56Z"
}

7. Проверка остатков

Эндпоинт: GET /products/1/

Пример ответа:

{
    "id": 1,
    "name": "Ноутбуки",
    "warehouse": 1,
    "quantity": 40  # (50 поставлено - 10 забрано)
}

Ограничения

1)Поставщик (provider) может только:

  Создавать транзакции типа supply

  Видеть список товаров

2)Потребитель (consumer) может только:

  Создавать транзакции типа consume

 Забирать не больше, чем есть на складе

  Ошибки:

  400 Bad Request: Попытка забрать больше товара, чем есть

  403 Forbidden: Несоответствие типа пользователя операции
  
Тестирование

Используйте инструменты:

  Postman / Insomnia для ручных запросов

  curl для CLI:
  curl -X POST http://localhost:8000/transactions/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"product": 1, "transaction_type": "supply", "quantity": 30}'
