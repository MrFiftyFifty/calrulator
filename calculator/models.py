from django.db import models
from django.contrib.auth.models import User


class CalculationHistory(models.Model):
    """Model to store calculation history."""
    
    OPERATION_CHOICES = [
        ('add', 'Сложение'),
        ('subtract', 'Вычитание'),
        ('multiply', 'Умножение'),
        ('divide', 'Деление'),
        ('power', 'Возведение в степень'),
        ('sqrt', 'Квадратный корень'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', related_name='calculations')
    num1 = models.FloatField(verbose_name='Первое число')
    num2 = models.FloatField(verbose_name='Второе число', null=True, blank=True)
    operation = models.CharField(max_length=20, choices=OPERATION_CHOICES, verbose_name='Операция')
    result = models.FloatField(verbose_name='Результат')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'История вычислений'
        verbose_name_plural = 'История вычислений'
    
    def __str__(self):
        if self.num2 is not None:
            return f"{self.num1} {self.get_operation_display()} {self.num2} = {self.result}"
        return f"{self.get_operation_display()}({self.num1}) = {self.result}"
    
    def get_operation_symbol(self):
        """Return operation symbol for display."""
        symbols = {
            'add': '+',
            'subtract': '−',
            'multiply': '×',
            'divide': '÷',
            'power': '^',
            'sqrt': '√',
        }
        return symbols.get(self.operation, self.operation)
