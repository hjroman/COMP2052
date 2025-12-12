# Arquitectura del Sistema

## Descripción General

El sistema de gestión de inventario sigue una arquitectura web tradicional de tres capas con el patrón **MVC (Model-View-Controller)**, adaptado para Flask.

---

## Diagrama de Arquitectura General

```
    ┌──────────────────┐
    │   NAVEGADOR WEB  │  <- Cliente (Usuario final)
    │  (Chrome, Edge)  │
    └────────┬─────────┘
             │
             │ HTTP Request (GET/POST)
             │
             ▼
    ┌────────────────────────────────────┐
    │      SERVIDOR FLASK                │
    │                                    │
    │  ┌──────────────────────────────┐  │
    │  │  Capa de Presentación        │  │
    │  │  (Jinja2 Templates + CSS)    │  │
    │  └─────────────┬────────────────┘  │
    │                │                   │
    │  ┌─────────────▼────────────────┐  │
    │  │  Capa de Aplicación          │  │
    │  │  (Flask Routes + Lógica)     │  │
    │  └─────────────┬────────────────┘  │
    │                │                   │
    │  ┌─────────────▼────────────────┐  │
    │  │  Capa de Datos               │  │
    │  │  (SQLAlchemy ORM)            │  │
    │  └─────────────┬────────────────┘  │
    └────────────────┼────────────────────┘
                     │
                     │ SQL Queries
                     ▼
    ┌────────────────────────────────────┐
    │   BASE DE DATOS SQLite             │
    │   (inventory.db)                   │
    │                                    │
    │   Tablas:                          │
    │   - suppliers (proveedores)        │
    │   - products (productos)           │
    └────────────────────────────────────┘
```

---

## Componentes de la Arquitectura

### 1. Capa de Presentación (Frontend)

**Tecnologías**: HTML5, CSS3, Jinja2

**Responsabilidades**:
- Renderizar la interfaz de usuario
- Mostrar formularios y tablas
- Presentar mensajes flash

### 2. Capa de Aplicación (Backend - Flask)

**Tecnologías**: Flask, Python

**Responsabilidades**:
- Procesar peticiones HTTP
- Validar datos
- Ejecutar lógica de negocio
- Generar respuestas

### 3. Capa de Acceso a Datos (ORM)

**Tecnologías**: SQLAlchemy

**Responsabilidades**:
- Mapear objetos Python a tablas
- Generar consultas SQL
- Gestionar conexiones

### 4. Base de Datos

**Tecnología**: SQLite

**Tablas**: suppliers, products

---

## Flujo de Datos Simplificado

```
1. NAVEGADOR
   └─> Solicita página (GET /products)

2. FLASK
   └─> Recibe petición en la ruta

3. SQLALCHEMY
   └─> Product.query.all()
   └─> Genera: SELECT * FROM products

4. SQLITE
   └─> Ejecuta la consulta SQL
   └─> Retorna los datos

5. SQLALCHEMY
   └─> Convierte datos a objetos Python

6. FLASK
   └─> Renderiza template con los datos

7. NAVEGADOR
   └─> Muestra la página HTML al usuario
```

**Flujo resumido:** Navegador → Flask → SQLAlchemy → SQLite → SQLAlchemy → Flask → Navegador

---

## Patrones de Diseño

### MVC (Model-View-Controller)

| Componente | Implementación |
|------------|----------------|
| **Model** | models.py (SQLAlchemy) |
| **View** | templates/*.html (Jinja2) |
| **Controller** | app.py (rutas Flask) |

---

## Seguridad

- **SQL Injection**: Prevenido por SQLAlchemy ORM
- **XSS**: Jinja2 escapa variables automáticamente
- **Validación**: Servidor valida todos los datos
- **Confirmaciones**: JavaScript confirma eliminaciones

---

## Resumen

**Navegador → Flask → SQLAlchemy → SQLite**

El sistema usa una arquitectura de 3 capas que separa la presentación, lógica de negocio y acceso a datos.
