from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('move/<int:tile>/', views.move_tile, name='move_tile'),
    path('reset/', views.reset, name='reset'),  # ✅ Added
]