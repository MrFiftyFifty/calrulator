import math
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import CalculationHistory
from .forms import RegisterForm, LoginForm


@login_required
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
                    user=request.user,
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


@login_required
def history_view(request):
    """Display calculation history."""
    # Base queryset - user sees only their own calculations
    # Admin sees all calculations
    if request.user.is_staff:
        history = CalculationHistory.objects.all()
    else:
        history = CalculationHistory.objects.filter(user=request.user)
    
    # Search
    search_query = request.GET.get('search', '')
    if search_query:
        history = history.filter(
            Q(num1__icontains=search_query) |
            Q(num2__icontains=search_query) |
            Q(result__icontains=search_query)
        )
    
    # Filter by operation
    operation_filter = request.GET.get('operation', '')
    if operation_filter:
        history = history.filter(operation=operation_filter)
    
    # Sort
    sort_by = request.GET.get('sort', '-timestamp')
    if sort_by:
        history = history.order_by(sort_by)
    
    # Limit to 50 results
    history = history[:50]
    
    context = {
        'history': history,
        'search_query': search_query,
        'operation_filter': operation_filter,
        'sort_by': sort_by,
        'operations': CalculationHistory.OPERATION_CHOICES,
    }
    
    return render(request, 'calculator/history.html', context)


@login_required
def clear_history(request):
    """Clear calculation history."""
    if request.method == 'POST':
        if request.user.is_staff:
            # Admin clears all history
            CalculationHistory.objects.all().delete()
            messages.success(request, 'История всех пользователей очищена')
        else:
            # User clears only their own history
            CalculationHistory.objects.filter(user=request.user).delete()
            messages.success(request, 'Ваша история очищена')
    
    return redirect('calculator:history')


def register_view(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('calculator:calculator')
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('calculator:calculator')
    else:
        form = RegisterForm()
    
    return render(request, 'calculator/register.html', {'form': form})


def login_view(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('calculator:calculator')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect(request.GET.get('next', 'calculator:calculator'))
    else:
        form = LoginForm()
    
    return render(request, 'calculator/login.html', {'form': form})


def logout_view(request):
    """User logout view."""
    logout(request)
    messages.success(request, 'Вы вышли из аккаунта')
    return redirect('calculator:login')
