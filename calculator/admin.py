from django.contrib import admin
from .models import CalculationHistory


@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    """Admin interface for CalculationHistory model."""
    
    list_display = ['id', 'user', 'num1', 'operation', 'num2', 'result', 'timestamp']
    list_filter = ['operation', 'timestamp', 'user']
    search_fields = ['user__username', 'num1', 'num2', 'result']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    def has_add_permission(self, request):
        """Disable manual addition through admin."""
        return False
