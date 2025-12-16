from django.contrib import admin
from .models import CalculationHistory


@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    """Admin interface for CalculationHistory model."""
    
    list_display = ['id', 'num1', 'operation', 'num2', 'result', 'timestamp']
    list_filter = ['operation', 'timestamp']
    search_fields = ['num1', 'num2', 'result']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        """Disable manual addition through admin."""
        return False
