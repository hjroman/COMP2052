# Sistema de Gestión de Inventario

Aplicación web para gestión de inventario desarrollada con Flask y SQLAlchemy.

## Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar la aplicación
python app.py

# 3. Abrir en el navegador
# http://127.0.0.1:5000
```

## Características

- ✅ Gestión completa de proveedores (CRUD)
- ✅ Gestión completa de productos (CRUD)
- ✅ Filtrado de productos por proveedor
- ✅ Reporte de stock bajo configurable
- ✅ Validaciones de datos
- ✅ Interfaz web responsive

## Documentación

Toda la documentación del proyecto se encuentra en la carpeta [`docs/`](docs/):

- **[README_PROYECTO.md](docs/README_PROYECTO.md)** - Guía completa del proyecto
- **[modelos_bd.md](docs/modelos_bd.md)** - Estructura de base de datos
- **[endpoints.md](docs/endpoints.md)** - Referencia de rutas/API
- **[arquitectura.md](docs/arquitectura.md)** - Arquitectura del sistema

## Estructura del Proyecto

```
inventory_app/
├── app.py                    # Aplicación principal
├── models.py                 # Modelos de base de datos
├── config.py                 # Configuración
├── requirements.txt          # Dependencias
├── templates/                # Plantillas HTML
├── static/                   # Archivos estáticos (CSS)
├── docs/                     # Documentación
└── instance/                 # Base de datos SQLite
```

## Tecnologías

- **Backend**: Flask 3.1.2
- **ORM**: SQLAlchemy 2.0.44
- **Base de Datos**: SQLite
- **Frontend**: HTML5, CSS3, Jinja2

## Requisitos

- Python 3.7+
- pip

## Licencia

Proyecto académico - COMP2052
