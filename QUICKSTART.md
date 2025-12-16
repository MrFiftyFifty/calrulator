# Быстрый старт

## Установка и запуск

```bash
# 1. Активировать виртуальное окружение (если еще не активировано)
source venv/bin/activate

# 2. Запустить сервер
python manage.py runserver
```

## Доступные URL

### Веб-интерфейс
- **Калькулятор**: http://127.0.0.1:8000/
- **История**: http://127.0.0.1:8000/history/
- **Админ-панель**: http://127.0.0.1:8000/admin/

### API Endpoints
- **Получить JWT токен**: `POST http://127.0.0.1:8000/api/token/`
- **Обновить токен**: `POST http://127.0.0.1:8000/api/token/refresh/`
- **Вычисление**: `POST http://127.0.0.1:8000/api/calculate/`
- **История**: `GET http://127.0.0.1:8000/api/history/`
- **Очистить историю**: `DELETE http://127.0.0.1:8000/api/history/clear/`

## Тестирование API

```bash
# Установить requests (если еще не установлено)
pip install requests

# Запустить тесты API
python test_api.py
```

## Тестовые данные

**Пользователь для API:**
- Username: `testuser`
- Password: `testpass123`

## Поддерживаемые операции

1. **add** - Сложение (num1 + num2)
2. **subtract** - Вычитание (num1 - num2)
3. **multiply** - Умножение (num1 × num2)
4. **divide** - Деление (num1 ÷ num2)
5. **power** - Возведение в степень (num1 ^ num2)
6. **sqrt** - Квадратный корень (√num1)

## Быстрый тест через curl

```bash
# 1. Получить токен
TOKEN=$(curl -s -X POST http://127.0.0.1:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access'])")

# 2. Выполнить вычисление
curl -X POST http://127.0.0.1:8000/api/calculate/ \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"num1": 10, "num2": 5, "operation": "add"}'

# 3. Получить историю
curl -X GET http://127.0.0.1:8000/api/history/ \
  -H "Authorization: Bearer $TOKEN"
```

## Уровни сложности задания

✅ **Уровень 1** - Простой калькулятор  
✅ **Уровень 2** - Калькулятор с историей операций  
✅ **Уровень 3** - API с JWT токенами (самый сложный)

Проект выполнен на **максимальном уровне сложности** (Уровень 3).
