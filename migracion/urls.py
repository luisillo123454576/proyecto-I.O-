from django.urls import path
from . import views

app_name = 'migracion'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/optimizar/', views.api_optimizar, name='api_optimizar'),
    path('api/simular/', views.api_simular, name='api_simular'),
    path('api/recalcular/', views.api_recalcular, name='api_recalcular'),
    path('codigo/', views.vista_codigo, name='vista_codigo'),
    path('documentacion/', views.vista_documentacion, name='vista_documentacion'),
    path('documentacion/<str:doc_id>/', views.vista_documentacion, name='vista_documentacion_doc'),
]

