from django.urls import path, include
from . import views

app_name = 'calculator'

urlpatterns = [
    # Web interface
    path('', views.calculator, name='calculator'),
    path('history/', views.history_view, name='history'),
    path('history/clear/', views.clear_history, name='clear_history'),
    
    # API endpoints
    path('api/', include('calculator.api_urls')),
]
