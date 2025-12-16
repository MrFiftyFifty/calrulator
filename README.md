# Django Calculator с JWT API

Веб-калькулятор на Django с историей операций и REST API с JWT токенами.

## Возможности

**Веб-интерфейс:**
- Аутентификация пользователей (регистрация/вход/выход)
- Операции: +, -, ×, ÷, xⁿ, √
- Личная история вычислений (до 50 записей)
- Фильтрация, поиск и сортировка истории
- Админ: просмотр всех операций пользователей

**REST API:**
- JWT аутентификация
- Привязка операций к пользователям
- CRUD операции через API

## Установка

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Использование

**Регистрация:** http://127.0.0.1:8000/register/  
**Вход:** http://127.0.0.1:8000/login/  
**Калькулятор:** http://127.0.0.1:8000/  
**История:** http://127.0.0.1:8000/history/  
**Админ:** http://127.0.0.1:8000/admin/

### Тестовые пользователи

**Админ:**
- Username: `admin`
- Password: `admin123`

**Пользователи:**
- user1 / password123
- user2 / password123

## API

**Base URL:** `http://127.0.0.1:8000/api/`

### Аутентификация

```bash
# Получить токен
POST /api/token/
{"username": "testuser", "password": "testpass123"}

# Обновить токен
POST /api/token/refresh/
{"refresh": "<refresh_token>"}
```

### Endpoints (требуют JWT токен)

```bash
# Вычисление
POST /api/calculate/
{"num1": 10, "num2": 5, "operation": "add"}
# Операции: add, subtract, multiply, divide, power, sqrt

# История
GET /api/history/

# Очистить историю
DELETE /api/history/clear/
```

## Тестирование API

```bash
# Автоматические тесты
python test_api.py
```

**API Тестовый пользователь:**  
Username: `user1`  
Password: `password123`

## Технологии

Django 5.2.9, DRF 3.16.1, JWT, SQLite
