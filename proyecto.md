# Cómo agregar un nuevo CRUD al proyecto

Si el profesor pide una entidad nueva (Departamentos, Categorías, etc.), no crear un proyecto Django nuevo: agregar una app dentro de este mismo proyecto, copiando el patrón que ya usa `billing` (por ejemplo `Brand` o `Customer`, son los CRUD más simples para duplicar).

## Pasos

1. **Crear la app**
   ```
   python manage.py startapp nombre_app
   ```

2. **Registrarla en `config/settings.py` → `INSTALLED_APPS`**

3. **Modelo** (`models.py`)
   ```python
   class Departamento(models.Model):
       nombre = models.CharField(max_length=100)
       descripcion = models.TextField()

       def __str__(self):
           return self.nombre
   ```

4. **Migraciones**
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Formulario** (`forms.py`)
   ```python
   from django.forms import ModelForm
   from .models import Departamento

   class DepartamentoForm(ModelForm):
       class Meta:
           model = Departamento
           fields = "__all__"
   ```

6. **Vistas CRUD** (listar, crear, editar, eliminar) — usar Class Based Views, igual que el resto del proyecto.

7. **URLs**
   ```python
   urlpatterns = [
       path("", DepartamentoListView.as_view(), name="departamento_list"),
       path("new/", DepartamentoCreateView.as_view(), name="departamento_create"),
       path("<int:pk>/edit/", DepartamentoUpdateView.as_view(), name="departamento_update"),
       path("<int:pk>/delete/", DepartamentoDeleteView.as_view(), name="departamento_delete"),
   ]
   ```

8. **Templates** en `templates/nombre_app/`: `_list.html`, `_form.html`, `_confirm_delete.html`

9. **Agregar el enlace al menú** en `base.html`

10. **Probar**: crear, editar, eliminar, buscar, validaciones.

## Qué ya tiene `billing` como referencia
Modelo, formularios, vistas, URLs, templates, confirmación de eliminar, validaciones, diseño Bootstrap — el patrón completo. Copiar la estructura de `Brand` o `Customer`, cambiar nombre de modelo/campos, y ajustar templates.
