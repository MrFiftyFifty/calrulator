import math
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import CalculationHistory


def calculator(request):
    """Main calculator view."""
    result = None
    error = None
    
    if request.method == 'POST':
        try:
            num1 = float(request.POST.get('num1', 0))
            operation = request.POST.get('operation')
            num2 = None
            
            # For sqrt operation, num2 is not needed
            if operation != 'sqrt':
                num2 = float(request.POST.get('num2', 0))
            
            # Perform calculation
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
            elif operation == 'power':
                result = num1 ** num2
            elif operation == 'sqrt':
                if num1 < 0:
                    error = 'Нельзя извлечь корень из отрицательного числа'
                else:
                    result = math.sqrt(num1)
            else:
                error = 'Неизвестная операция'
            
            # Save to history if calculation was successful
            if result is not None and error is None:
                CalculationHistory.objects.create(
                    num1=num1,
                    num2=num2,
                    operation=operation,
                    result=result
                )
                
        except ValueError:
            error = 'Пожалуйста, введите корректные числа'
        except Exception as e:
            error = f'Ошибка: {str(e)}'
    
    context = {
        'result': result,
        'error': error,
    }
    
    return render(request, 'calculator/calculator.html', context)


def history_view(request):
    """Display calculation history."""
    history = CalculationHistory.objects.all()[:10]
    
    context = {
        'history': history,
    }
    
    return render(request, 'calculator/history.html', context)


def clear_history(request):
    """Clear all calculation history."""
    if request.method == 'POST':
        CalculationHistory.objects.all().delete()
        messages.success(request, 'История очищена')
    
    return redirect('calculator:history')
