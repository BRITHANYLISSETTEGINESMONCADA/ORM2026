from django.urls import path
from . import views

app_name = 'tareas'

urlpatterns = [
    path('', views.tareas_list, name='list'),
    path('crear/', views.tareas_create, name='create'),
    path('<int:task_id>/', views.tareas_detail, name='detail'),
    path('<int:task_id>/complete/', views.tareas_complete, name='complete'),
    path('<int:task_id>/delete/', views.tareas_delete, name='delete'),
]
