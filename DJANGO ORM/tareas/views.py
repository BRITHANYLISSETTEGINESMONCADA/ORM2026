"""Vistas wrapper para `tareas` que reutilizan la lógica de `tasks.views`.
Esto evita mover modelos/tabla y preserva datos existentes.
"""
from tasks import views as tasks_views


def tareas_list(request):
    return tasks_views.tasks(request)


def tareas_create(request):
    return tasks_views.create_task(request)


def tareas_detail(request, task_id):
    return tasks_views.task_detail(request, task_id=task_id)


def tareas_complete(request, task_id):
    return tasks_views.complete_task(request, task_id=task_id)


def tareas_delete(request, task_id):
    return tasks_views.delete_task(request, task_id=task_id)
