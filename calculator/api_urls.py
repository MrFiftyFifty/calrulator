from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import CalculatorAPIViewSet

# Create router-like URL patterns manually
calculator_calculate = CalculatorAPIViewSet.as_view({'post': 'calculate'})
calculator_history = CalculatorAPIViewSet.as_view({'get': 'history'})
calculator_clear_history = CalculatorAPIViewSet.as_view({'delete': 'clear_history'})

urlpatterns = [
    # JWT Authentication endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Calculator API endpoints
    path('calculate/', calculator_calculate, name='api_calculate'),
    path('history/', calculator_history, name='api_history'),
    path('history/clear/', calculator_clear_history, name='api_clear_history'),
]
