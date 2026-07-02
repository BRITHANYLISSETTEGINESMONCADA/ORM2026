from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone

from .forms import CargoForm, EmpleadoForm, SigninForm, SignupForm, TaskForm
from .models import Cargo, Empleado, Task


def home(request):
    return render(request, 'home.html', task_stats(request.user))


def task_stats(user):
    if not user.is_authenticated:
        return {}

    user_tasks = Task.objects.filter(user=user)
    return {
        'pending_count': user_tasks.filter(datecompleted__isnull=True).count(),
        'completed_count': user_tasks.filter(datecompleted__isnull=False).count(),
        'important_count': user_tasks.filter(
            important=True,
            datecompleted__isnull=True,
        ).count(),
    }


def process_form_view(request, form_class, template_name, success_url, instance=None, extra_context=None):
    if request.method == 'GET':
        form = form_class(instance=instance)
    else:
        form = form_class(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            return redirect(success_url)

    context = {
        'form': form,
    }
    if instance is not None:
        context[instance.__class__.__name__.lower()] = instance
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context)


def process_delete_view(request, instance, template_name, success_url, extra_context=None):
    if request.method == 'POST':
        instance.delete()
        return redirect(success_url)

    context = {
        'object': instance,
    }
    if extra_context:
        context.update(extra_context)
    return render(request, template_name, context)


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': SignupForm()})

    if request.POST['password1'] != request.POST['password2']:
        return render(request, 'signup.html', {
            'form': SignupForm(),
            'error': 'Las contraseñas no coinciden',
        })

    try:
        user = User.objects.create_user(
            username=request.POST['username'],
            password=request.POST['password1'],
        )
        user.save()
        login(request, user)
        return redirect('tasks')
    except IntegrityError:
        return render(request, 'signup.html', {
            'form': SignupForm(),
            'error': 'El usuario ya existe',
        })


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': SigninForm()})

    user = authenticate(
        request,
        username=request.POST['username'],
        password=request.POST['password'],
    )

    if user is None:
        return render(request, 'signin.html', {
            'form': SigninForm(),
            'error': 'El usuario o la contraseña son incorrectos',
        })

    login(request, user)
    return redirect('tasks')


def signout(request):
    logout(request)
    return redirect('home')


@login_required
def tasks(request):
    user_tasks = Task.objects.filter(
        user=request.user,
        datecompleted__isnull=True,
    ).order_by('-important', '-created')
    return render(request, 'tasks.html', {
        'tasks': user_tasks,
        'completed_view': False,
        **task_stats(request.user),
    })


@login_required
def tasks_completed(request):
    user_tasks = Task.objects.filter(
        user=request.user,
        datecompleted__isnull=False,
    ).order_by('-datecompleted')
    return render(request, 'tasks.html', {
        'tasks': user_tasks,
        'completed_view': True,
        **task_stats(request.user),
    })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm()})

    try:
        form = TaskForm(request.POST)
        if form.is_valid():
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
    except ValueError:
        form = TaskForm()

    return render(request, 'create_task.html', {
        'form': form,
        'error': 'Por favor, proporciona datos válidos',
    })


@login_required
def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'GET':
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task': task, 'form': form})

    try:
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks')
    except ValueError:
        form = TaskForm(instance=task)

    return render(request, 'task_detail.html', {
        'task': task,
        'form': form,
        'error': 'Error actualizando la tarea',
    })


@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')
    return redirect('task_detail', task_id=task.id)


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    return redirect('task_detail', task_id=task.id)


@login_required
def cargo_list(request):
    cargos = Cargo.objects.all()
    return render(request, 'cargo_list.html', {
        'cargos': cargos,
        'view_type': 'VBF',
    })


@login_required
def cargo_create(request):
    return process_form_view(
        request,
        CargoForm,
        'form.html',
        'cargo_list',
        extra_context={'view_type': 'VBF', 'title': 'Nuevo Cargo', 'cancel_url': reverse_lazy('cargo_list')},
    )


@login_required
def cargo_update(request, cargo_id):
    cargo = get_object_or_404(Cargo, pk=cargo_id)
    return process_form_view(
        request,
        CargoForm,
        'form.html',
        'cargo_list',
        instance=cargo,
        extra_context={'view_type': 'VBF', 'title': 'Editar Cargo', 'cancel_url': reverse_lazy('cargo_list')},
    )


@login_required
def cargo_delete(request, cargo_id):
    cargo = get_object_or_404(Cargo, pk=cargo_id)
    return process_delete_view(
        request,
        cargo,
        'confirm_delete.html',
        'cargo_list',
        extra_context={
            'view_type': 'VBF',
            'title': 'Eliminar Cargo',
            'question': f'¿Seguro que quieres eliminar el cargo "{cargo.nombre}"?',
            'cancel_url': reverse_lazy('cargo_list'),
        },
    )


@login_required
def empleado_list(request):
    empleados = Empleado.objects.select_related('cargo').all()
    return render(request, 'empleado_list.html', {
        'empleados': empleados,
        'view_type': 'VBF',
    })


@login_required
def empleado_create(request):
    return process_form_view(
        request,
        EmpleadoForm,
        'form.html',
        'empleado_list',
        extra_context={'view_type': 'VBF', 'title': 'Nuevo Empleado', 'cancel_url': reverse_lazy('empleado_list')},
    )


@login_required
def empleado_update(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    return process_form_view(
        request,
        EmpleadoForm,
        'form.html',
        'empleado_list',
        instance=empleado,
        extra_context={'view_type': 'VBF', 'title': 'Editar Empleado', 'cancel_url': reverse_lazy('empleado_list')},
    )


@login_required
def empleado_delete(request, empleado_id):
    empleado = get_object_or_404(Empleado, pk=empleado_id)
    return process_delete_view(
        request,
        empleado,
        'confirm_delete.html',
        'empleado_list',
        extra_context={
            'view_type': 'VBF',
            'title': 'Eliminar Empleado',
            'question': f'¿Seguro que deseas eliminar a {empleado.nombres} {empleado.apellidos}?',
            'cancel_url': reverse_lazy('empleado_list'),
        },
    )


