from django.shortcuts import render


def calculator(request):
    """Main calculator view."""
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            num2 = float(request.POST.get('num2', 0))
            operation = request.POST.get('operation')
            
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                if num2 == 0:
                    error = 'Деление на ноль невозможно'
                else:
                    result = num1 / num2
            else:
                error = 'Неизвестная операция'
                
        except ValueError:
            error = 'Пожалуйста, введите корректные числа'
        except Exception as e:
            error = f'Ошибка: {str(e)}'
    
    context = {
        'result': result,
        'error': error,
    }
    
    return render(request, 'calculator/calculator.html', context)
