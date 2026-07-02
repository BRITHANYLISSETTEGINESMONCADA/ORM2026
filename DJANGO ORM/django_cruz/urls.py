"""
URL configuration for django_cruz project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tasks import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='signout'),

    path('tasks/', views.tasks, name='tasks'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/completed/', views.tasks_completed, name='tasks_completed'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/complete/', views.complete_task, name='complete_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),

    path('cargo/', views.cargo_list, name='cargo_list'),
    path('cargo/nuevo/', views.cargo_create, name='cargo_create'),
    path('cargo/<int:cargo_id>/editar/', views.cargo_update, name='cargo_update'),
    path('cargo/<int:cargo_id>/eliminar/', views.cargo_delete, name='cargo_delete'),

    # Rutas plurales (compatibilidad y consistencia)
    path('cargos/', views.cargo_list, name='cargos_list'),
    path('cargos/nuevo/', views.cargo_create, name='cargos_create'),
    path('cargos/<int:cargo_id>/editar/', views.cargo_update, name='cargos_update'),
    path('cargos/<int:cargo_id>/eliminar/', views.cargo_delete, name='cargos_delete'),

    # Rutas CBV eliminadas para simplificar la app

    path('tareas/', include('tareas.urls')),

    path('empleado/', views.empleado_list, name='empleado_list'),
    path('empleado/nuevo/', views.empleado_create, name='empleado_create'),
    path('empleado/<int:empleado_id>/editar/', views.empleado_update, name='empleado_update'),
    path('empleado/<int:empleado_id>/eliminar/', views.empleado_delete, name='empleado_delete'),

    # Rutas plurales para empleados
    path('empleados/', views.empleado_list, name='empleados_list'),
    path('empleados/nuevo/', views.empleado_create, name='empleados_create'),
    path('empleados/<int:empleado_id>/editar/', views.empleado_update, name='empleados_update'),
    path('empleados/<int:empleado_id>/eliminar/', views.empleado_delete, name='empleados_delete'),

    # Rutas CBV eliminadas para simplificar la app
]
