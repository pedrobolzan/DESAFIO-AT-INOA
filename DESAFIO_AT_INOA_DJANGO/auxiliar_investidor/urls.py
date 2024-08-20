from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('criar/', views.create_ativo, name='create_ativo'),
    path('editar/<int:ativo_id>/', views.update_ativo, name='update_ativo'),
    path('cotacoes/<int:ativo_id>/', views.get_cotacoes, name='get_cotacoes'),
]
