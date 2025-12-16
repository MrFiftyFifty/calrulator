#!/usr/bin/env python
"""
Скрипт для тестирования Calculator API с JWT аутентификацией.
Запуск: python test_api.py
"""

import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

# Цвета для вывода
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'


def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")


def print_error(message):
    print(f"{RED}✗ {message}{RESET}")


def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")


def print_response(response):
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except:
        print(f"Response: {response.text}")
    print()


def test_api():
    print("=" * 60)
    print("Тестирование Calculator API с JWT")
    print("=" * 60)
    print()
    
    # 1. Получение JWT токена
    print_info("1. Получение JWT токена...")
    try:
        response = requests.post(
            f"{BASE_URL}/token/",
            json={
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        if response.status_code == 200:
            tokens = response.json()
            access_token = tokens['access']
            refresh_token = tokens['refresh']
            print_success("Токен получен успешно")
            print_response(response)
        else:
            print_error(f"Не удалось получить токен")
            print_response(response)
            return
    except Exception as e:
        print_error(f"Ошибка: {e}")
        return
    
    # Заголовки с токеном
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # 2. Тест операции сложения
    print_info("2. Тестирование операции сложения (10 + 5)...")
    try:
        response = requests.post(
            f"{BASE_URL}/calculate/",
            headers=headers,
            json={
                "num1": 10,
                "num2": 5,
                "operation": "add"
            }
        )
        
        if response.status_code == 200:
            print_success("Сложение выполнено успешно")
        else:
            print_error("Ошибка при сложении")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 3. Тест операции умножения
    print_info("3. Тестирование операции умножения (7 × 8)...")
    try:
        response = requests.post(
            f"{BASE_URL}/calculate/",
            headers=headers,
            json={
                "num1": 7,
                "num2": 8,
                "operation": "multiply"
            }
        )
        
        if response.status_code == 200:
            print_success("Умножение выполнено успешно")
        else:
            print_error("Ошибка при умножении")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 4. Тест операции деления
    print_info("4. Тестирование операции деления (20 ÷ 4)...")
    try:
        response = requests.post(
            f"{BASE_URL}/calculate/",
            headers=headers,
            json={
                "num1": 20,
                "num2": 4,
                "operation": "divide"
            }
        )
        
        if response.status_code == 200:
            print_success("Деление выполнено успешно")
        else:
            print_error("Ошибка при делении")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 5. Тест операции возведения в степень
    print_info("5. Тестирование операции возведения в степень (2^10)...")
    try:
        response = requests.post(
            f"{BASE_URL}/calculate/",
            headers=headers,
            json={
                "num1": 2,
                "num2": 10,
                "operation": "power"
            }
        )
        
        if response.status_code == 200:
            print_success("Возведение в степень выполнено успешно")
        else:
            print_error("Ошибка при возведении в степень")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 6. Тест операции квадратного корня
    print_info("6. Тестирование операции квадратного корня (√144)...")
    try:
        response = requests.post(
            f"{BASE_URL}/calculate/",
            headers=headers,
            json={
                "num1": 144,
                "operation": "sqrt"
            }
        )
        
        if response.status_code == 200:
            print_success("Квадратный корень вычислен успешно")
        else:
            print_error("Ошибка при вычислении квадратного корня")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 7. Тест деления на ноль (должна быть ошибка)
    print_info("7. Тестирование деления на ноль (должна быть ошибка)...")
    try:
        response = requests.post(
            f"{BASE_URL}/calculate/",
            headers=headers,
            json={
                "num1": 10,
                "num2": 0,
                "operation": "divide"
            }
        )
        
        if response.status_code == 400:
            print_success("Ошибка корректно обработана")
        else:
            print_error("Неожиданный статус код")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 8. Получение истории операций
    print_info("8. Получение истории операций...")
    try:
        response = requests.get(
            f"{BASE_URL}/history/",
            headers=headers
        )
        
        if response.status_code == 200:
            history = response.json()
            print_success(f"Получено записей в истории: {len(history)}")
        else:
            print_error("Ошибка при получении истории")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 9. Обновление токена
    print_info("9. Тестирование обновления токена...")
    try:
        response = requests.post(
            f"{BASE_URL}/token/refresh/",
            json={
                "refresh": refresh_token
            }
        )
        
        if response.status_code == 200:
            new_token = response.json()
            print_success("Токен обновлен успешно")
        else:
            print_error("Ошибка при обновлении токена")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    # 10. Тест без токена (должна быть ошибка 401)
    print_info("10. Тестирование без токена (должна быть ошибка 401)...")
    try:
        response = requests.get(f"{BASE_URL}/history/")
        
        if response.status_code == 401:
            print_success("Аутентификация работает корректно")
        else:
            print_error("Неожиданный статус код")
        print_response(response)
    except Exception as e:
        print_error(f"Ошибка: {e}\n")
    
    print("=" * 60)
    print("Тестирование завершено!")
    print("=" * 60)


if __name__ == "__main__":
    print("\nУбедитесь, что сервер запущен: python manage.py runserver\n")
    
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\nТестирование прервано пользователем")
    except Exception as e:
        print(f"\n{RED}Критическая ошибка: {e}{RESET}")
