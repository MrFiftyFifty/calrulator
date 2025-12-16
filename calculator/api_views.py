import math
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import CalculationHistory
from .serializers import (
    CalculationHistorySerializer,
    CalculateSerializer,
    CalculationResultSerializer
)


class CalculatorAPIViewSet(viewsets.ViewSet):
    """API ViewSet for calculator operations."""
    
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """
        Perform calculation.
        
        Expected input:
        {
            "num1": 10,
            "num2": 5,
            "operation": "add"
        }
        """
        serializer = CalculateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {'error': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        num1 = serializer.validated_data['num1']
        num2 = serializer.validated_data.get('num2')
        operation = serializer.validated_data['operation']
        
        # Perform calculation
        result = None
        
        try:
            if operation == 'add':
                result = num1 + num2
            elif operation == 'subtract':
                result = num1 - num2
            elif operation == 'multiply':
                result = num1 * num2
            elif operation == 'divide':
                result = num1 / num2
            elif operation == 'power':
                result = num1 ** num2
            elif operation == 'sqrt':
                result = math.sqrt(num1)
            
            # Save to history
            history_entry = CalculationHistory.objects.create(
                num1=num1,
                num2=num2,
                operation=operation,
                result=result
            )
            
            # Prepare response
            response_data = {
                'num1': num1,
                'num2': num2,
                'operation': operation,
                'operation_display': history_entry.get_operation_display(),
                'result': result,
                'history_id': history_entry.id
            }
            
            result_serializer = CalculationResultSerializer(response_data)
            
            return Response(
                result_serializer.data,
                status=status.HTTP_200_OK
            )
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get calculation history (last 10 entries)."""
        history = CalculationHistory.objects.all()[:10]
        serializer = CalculationHistorySerializer(history, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['delete'])
    def clear_history(self, request):
        """Clear all calculation history."""
        deleted_count = CalculationHistory.objects.all().count()
        CalculationHistory.objects.all().delete()
        
        return Response(
            {'message': f'Deleted {deleted_count} entries'},
            status=status.HTTP_200_OK
        )
