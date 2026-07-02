# Proyecto Django — django_cruz

Resumen rápido:
- App principal: `tasks` (contiene modelos `Task`, `Cargo`, `Empleado`)
- App adicional creada: `tareas` (wrappers seguros para `Task`, sin mover datos)

Requisitos
- Python 3.10+ (se probó en 3.14 en el entorno del autor)
- Virtualenv

Instalación y ejecución local

```powershell
# Activar venv (Windows PowerShell)
& .\.venv\Scripts\Activate.ps1

# Instalar dependencias (si no están ya instaladas)
python -m pip install -r requirements.txt

# Crear migraciones y migrar (no deberían generarse cambios si ya existen)
python manage.py makemigrations
python manage.py migrate

# Ejecutar servidor de desarrollo
python manage.py runserver
```

Pruebas básicas a realizar manualmente
- Registrar usuario (`/signup/`) y acceder con `/signin/`.
- Crear/editar/eliminar `Cargo` y `Empleado` desde `/cargos/` y `/empleados/`.
- Manejar `Task` desde `/tasks/` o `/tareas/` (wrappers disponibles en `/tareas/`).

Despliegue (recomendaciones)
- Usar `dj-database-url` para configurar la base de datos por `DATABASE_URL`.
- Usar `whitenoise` para servir archivos estáticos en producción.
- Usar `gunicorn` como servidor WSGI (ej: `gunicorn django_cruz.wsgi`).
- Configurar `SECRET_KEY` y `DEBUG=False` en variables de entorno.

Notas del mantenimiento
- Las rutas plurales `/cargos/` y `/empleados/` se añadieron por consistencia; las rutas originales se mantienen por compatibilidad.
- La app `tareas` fue añadida como paso intermedio para separar responsabilidades sin mover modelos ni tablas.

Contacto
- Si quieres que automatice la migración completa (mover `Task` a una app dedicada y transferir las tablas), dime y prepararé un plan paso a paso que preserve datos.
