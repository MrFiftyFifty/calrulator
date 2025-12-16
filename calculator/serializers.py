from rest_framework import serializers
from .models import CalculationHistory


class CalculationHistorySerializer(serializers.ModelSerializer):
    """Serializer for calculation history."""
    
    operation_display = serializers.CharField(source='get_operation_display', read_only=True)
    operation_symbol = serializers.CharField(source='get_operation_symbol', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = CalculationHistory
        fields = ['id', 'username', 'num1', 'num2', 'operation', 'operation_display', 'operation_symbol', 'result', 'timestamp']
        read_only_fields = ['id', 'username', 'timestamp']


class CalculateSerializer(serializers.Serializer):
    """Serializer for calculation input."""
    
    num1 = serializers.FloatField(required=True)
    num2 = serializers.FloatField(required=False, allow_null=True)
    operation = serializers.ChoiceField(
        choices=['add', 'subtract', 'multiply', 'divide', 'power', 'sqrt'],
        required=True
    )
    
    def validate(self, data):
        """Validate input data."""
        operation = data.get('operation')
        
        # sqrt only needs num1
        if operation == 'sqrt':
            if data.get('num1') is not None and data.get('num1') < 0:
                raise serializers.ValidationError('Cannot calculate square root of negative number')
        else:
            # All other operations need num2
            if data.get('num2') is None:
                raise serializers.ValidationError('num2 is required for this operation')
            
            # Check division by zero
            if operation == 'divide' and data.get('num2') == 0:
                raise serializers.ValidationError('Division by zero is not allowed')
        
        return data


class CalculationResultSerializer(serializers.Serializer):
    """Serializer for calculation result."""
    
    num1 = serializers.FloatField()
    num2 = serializers.FloatField(allow_null=True)
    operation = serializers.CharField()
    operation_display = serializers.CharField()
    result = serializers.FloatField()
    history_id = serializers.IntegerField()
