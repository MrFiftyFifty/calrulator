# Django Calculator с JWT API

Веб-калькулятор на Django с историей операций и REST API с JWT аутентификацией.

## Возможности

### Веб-интерфейс
- ✅ Базовые операции: сложение, вычитание, умножение, деление
- ✅ Дополнительные операции: возведение в степень, квадратный корень
- ✅ История последних 10 вычислений
- ✅ Очистка истории
- ✅ Валидация ввода и обработка ошибок
- ✅ Красивый адаптивный интерфейс

### REST API
- ✅ JWT аутентификация
- ✅ Выполнение вычислений через API
- ✅ Получение истории операций
- ✅ Очистка истории

## Установка

### 1. Клонирование репозитория
```bash
git clone <repository-url>
cd calculator_project
```

### 2. Создание виртуального окружения
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Применение миграций
```bash
python manage.py migrate
```

### 5. Создание суперпользователя (опционально)
```bash
python manage.py createsuperuser
```

### 6. Запуск сервера
```bash
python manage.py runserver
```

Приложение будет доступно по адресу: http://127.0.0.1:8000/

## Использование веб-интерфейса

1. **Калькулятор**: http://127.0.0.1:8000/
   - Введите первое число
   - Выберите операцию
   - Введите второе число (не требуется для √)
   - Нажмите "Вычислить"

2. **История операций**: http://127.0.0.1:8000/history/
   - Просмотр последних 10 вычислений
   - Кнопка очистки истории

3. **Админ-панель**: http://127.0.0.1:8000/admin/
   - Управление пользователями
   - Просмотр истории вычислений

## API Документация

### Базовый URL
```
http://127.0.0.1:8000/api/
```

### Аутентификация

#### Получение токена
**POST** `/api/token/`

```json
{
  "username": "testuser",
  "password": "testpass123"
}
```

Ответ:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Обновление токена
**POST** `/api/token/refresh/`

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### API Endpoints

Все API endpoints требуют JWT токен в заголовке:
```
Authorization: Bearer <access_token>
```

#### 1. Выполнить вычисление
**POST** `/api/calculate/`

Тело запроса:
```json
{
  "num1": 10,
  "num2": 5,
  "operation": "add"
}
```

Операции: `add`, `subtract`, `multiply`, `divide`, `power`, `sqrt`

Для операции `sqrt` поле `num2` не требуется:
```json
{
  "num1": 16,
  "operation": "sqrt"
}
```

Ответ:
```json
{
  "num1": 10.0,
  "num2": 5.0,
  "operation": "add",
  "operation_display": "Сложение",
  "result": 15.0,
  "history_id": 1
}
```

#### 2. Получить историю операций
**GET** `/api/history/`

Ответ:
```json
[
  {
    "id": 1,
    "num1": 10.0,
    "num2": 5.0,
    "operation": "add",
    "operation_display": "Сложение",
    "operation_symbol": "+",
    "result": 15.0,
    "timestamp": "2025-12-16T13:00:00Z"
  }
]
```

#### 3. Очистить историю
**DELETE** `/api/history/clear/`

Ответ:
```json
{
  "message": "Deleted 10 entries"
}
```

## Примеры использования API

### С использованием curl

1. Получить токен:
```bash
curl -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

2. Выполнить вычисление:
```bash
curl -X POST http://127.0.0.1:8000/api/calculate/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{"num1": 10, "num2": 5, "operation": "add"}'
```

3. Получить историю:
```bash
curl -X GET http://127.0.0.1:8000/api/history/ \
  -H "Authorization: Bearer <access_token>"
```

### С использованием Python requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000/api"

# Получение токена
response = requests.post(f"{BASE_URL}/token/", json={
    "username": "testuser",
    "password": "testpass123"
})
token = response.json()["access"]

# Заголовки с токеном
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Выполнение вычисления
response = requests.post(f"{BASE_URL}/calculate/", 
    headers=headers,
    json={
        "num1": 10,
        "num2": 5,
        "operation": "multiply"
    }
)
print(response.json())

# Получение истории
response = requests.get(f"{BASE_URL}/history/", headers=headers)
print(response.json())
```

## Структура проекта

```
calculator_project/
├── calculator/                 # Приложение калькулятора
│   ├── migrations/            # Миграции БД
│   ├── templates/             # HTML шаблоны
│   │   └── calculator/
│   │       ├── base.html      # Базовый шаблон
│   │       ├── calculator.html # Страница калькулятора
│   │       └── history.html   # Страница истории
│   ├── admin.py               # Настройки админки
│   ├── api_urls.py            # URL маршруты для API
│   ├── api_views.py           # API ViewSets
│   ├── models.py              # Модель CalculationHistory
│   ├── serializers.py         # DRF Serializers
│   ├── urls.py                # URL маршруты
│   └── views.py               # Views для веб-интерфейса
├── calculator_project/         # Настройки проекта
│   ├── settings.py            # Настройки Django
│   └── urls.py                # Главные URL маршруты
├── manage.py                  # Django CLI
├── requirements.txt           # Зависимости
└── README.md                  # Документация
```

## Технологии

- Python 3.10+
- Django 5.2.9
- Django REST Framework 3.16.1
- djangorestframework-simplejwt 5.5.1
- SQLite (БД)

## Тестовый пользователь

Для тестирования API создан пользователь:
- **Username**: `testuser`
- **Password**: `testpass123`

## Обработка ошибок

### Веб-интерфейс
- Деление на ноль
- Корень из отрицательного числа
- Некорректный ввод данных

### API
Возвращает соответствующие HTTP коды:
- `200` - Успешно
- `400` - Ошибка валидации
- `401` - Не авторизован
- `500` - Серверная ошибка

## Лицензия

MIT

## Автор

Разработано для практической работы по Django
