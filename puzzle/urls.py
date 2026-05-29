from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('move/<int:tile>/', views.move_tile, name='move_tile'),
    path('reset/', views.reset, name='reset'),
    path('api/move/<int:tile>/', views.move_tile, name='api_move_tile'),
    path('api/reset/', views.reset, name='api_reset'),
    path('api/solve/', views.solve_puzzle, name='api_solve'),
    path('api/hint/', views.get_hint, name='api_hint'),
    path('api/ping/', views.ping, name='api_ping'),
]