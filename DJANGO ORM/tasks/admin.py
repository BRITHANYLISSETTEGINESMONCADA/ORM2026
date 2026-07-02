from django.contrib import admin
from .models import Cargo, Empleado, Task


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created',)
    list_display = ('title', 'user', 'important', 'datecompleted', 'created')
    list_filter = ('important', 'datecompleted')


class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')


class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombres', 'apellidos', 'correo', 'cargo')
    list_filter = ('cargo',)


admin.site.register(Cargo, CargoAdmin)
admin.site.register(Empleado, EmpleadoAdmin)
admin.site.register(Task, TaskAdmin)
