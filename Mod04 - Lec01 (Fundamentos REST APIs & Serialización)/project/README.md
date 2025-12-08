# 📚 Sistema Gestor de Biblioteca - Proyecto Capstone

## 📋 Descripción del Proyecto

Sistema integral de gestión de biblioteca desarrollado con Flask que incluye autenticación, autorización basada en roles, interfaz web completa con templates Jinja2, formularios HTML y REST API.

**Características principales:**
- ✅ Gestión de libros
- ✅ Gestión de miembros
- ✅ Control de préstamos
- ✅ Sistema de autenticación
- ✅ Roles de usuario (Admin y Bibliotecario)
- ✅ REST API completa
- ✅ Interfaz moderna y responsiva

---

## 📁 Estructura del Proyecto

```
biblioteca/
│
├── app.py                      # Aplicación principal Flask
├── requirements.txt            # Dependencias del proyecto
├── README.md                   # Este archivo
│
├── static/                     # Archivos estáticos
│   └── css/
│       └── style.css          # Estilos CSS
│
└── templates/                  # Templates HTML (Jinja2)
    ├── base.html              # Template base (herencia)
    ├── login.html             # Página de login
    ├── dashboard.html         # Dashboard principal
    ├── books.html             # Gestión de libros
    ├── members.html           # Gestión de miembros
    ├── loans.html             # Gestión de préstamos
    └── users.html             # Gestión de usuarios (admin)
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Crear la carpeta del proyecto
mkdir biblioteca
cd biblioteca
```

### Paso 2: Crear la Estructura de Carpetas

```bash
# Crear carpetas necesarias
mkdir static
mkdir static/css
mkdir templates
```

### Paso 3: Copiar los Archivos

Copiar cada archivo a su ubicación correspondiente:

- `app.py` → En la raíz del proyecto
- `requirements.txt` → En la raíz del proyecto
- `style.css` → En `static/css/`
- Templates HTML → En la carpeta `templates/`:
  - `base.html`
  - `login.html`
  - `dashboard.html`
  - `books.html`
  - `members.html`
  - `loans.html`
  - `users.html`

### Paso 4: Crear requirements.txt

Crear el archivo `requirements.txt` con el siguiente contenido:

```
Flask==3.0.0
flask-marshmallow==1.2.1
marshmallow==3.20.1
Werkzeug==3.0.0
```

### Paso 5: Instalar Dependencias

```bash
pip install -r requirements.txt
```

### Paso 6: Ejecutar la Aplicación

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

---

## 🔐 Credenciales de Acceso

### Usuarios Predefinidos

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `admin123` | Administrador | Acceso completo + gestión de usuarios |
| `bibliotecario` | `biblio123` | Bibliotecario | Gestión de libros, miembros y préstamos |

---

## 🎯 Funcionalidades del Sistema

### 1. Sistema de Autenticación

- **Login seguro** con hash de contraseñas (Werkzeug)
- **Sesiones persistentes** para mantener usuarios conectados
- **Logout** con limpieza de sesión
- **Protección de rutas** mediante decoradores

### 2. Gestión de Libros

**Funcionalidades:**
- ➕ Agregar nuevos libros
- 📋 Listar todos los libros
- 🗑️ Eliminar libros
- 📊 Ver estado de disponibilidad

**Campos del libro:**
- Título
- Autor
- ISBN
- Año de publicación
- Categoría
- Estado (Disponible/Prestado)

### 3. Gestión de Miembros

**Funcionalidades:**
- ➕ Registrar nuevos miembros
- 📋 Listar todos los miembros
- 🗑️ Eliminar miembros
- 📅 Ver fecha de registro

**Campos del miembro:**
- Nombre
- Apellido
- Correo electrónico
- Teléfono
- Fecha de registro

### 4. Gestión de Préstamos

**Funcionalidades:**
- ➕ Registrar nuevos préstamos
- 📋 Listar todos los préstamos
- ✅ Marcar como devuelto
- 🗑️ Eliminar préstamos
- 📊 Ver estado (Activo/Devuelto)

**Control automático:**
- Verifica disponibilidad del libro
- Actualiza estado del libro al prestar
- Libera el libro al devolver
- Registra fechas de préstamo y devolución

### 5. Gestión de Usuarios (Solo Admin)

**Funcionalidades:**
- ➕ Crear nuevos usuarios del sistema
- 📋 Listar usuarios
- 🗑️ Eliminar usuarios
- 🔒 Protección contra auto-eliminación

**Roles disponibles:**
- Administrador
- Bibliotecario

---

## 🌐 Rutas de la Aplicación

### Rutas de Autenticación

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| GET/POST | `/login` | Iniciar sesión | Público |
| GET | `/logout` | Cerrar sesión | Autenticado |
| GET | `/` | Redirección inicial | Público |

### Rutas de Páginas Web

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| GET | `/dashboard` | Dashboard principal | Autenticado |
| GET | `/books` | Gestión de libros | Autenticado |
| GET | `/members` | Gestión de miembros | Autenticado |
| GET | `/loans` | Gestión de préstamos | Autenticado |
| GET | `/users` | Gestión de usuarios | Admin |

### Rutas de Formularios

| Método | Ruta | Descripción | Acceso |
|--------|------|-------------|--------|
| POST | `/books/create` | Crear libro | Autenticado |
| POST | `/books/delete/<id>` | Eliminar libro | Autenticado |
| POST | `/members/create` | Crear miembro | Autenticado |
| POST | `/members/delete/<id>` | Eliminar miembro | Autenticado |
| POST | `/loans/create` | Crear préstamo | Autenticado |
| POST | `/loans/return/<id>` | Devolver libro | Autenticado |
| POST | `/loans/delete/<id>` | Eliminar préstamo | Autenticado |
| POST | `/users/create` | Crear usuario | Admin |
| POST | `/users/delete/<id>` | Eliminar usuario | Admin |

### Rutas API REST (JSON)

#### Libros
- `GET /api/books` - Listar todos los libros
- `GET /api/books/<id>` - Obtener libro específico
- `POST /api/books` - Crear libro
- `PUT /api/books/<id>` - Actualizar libro
- `DELETE /api/books/<id>` - Eliminar libro

#### Miembros
- `GET /api/members` - Listar todos los miembros
- `GET /api/members/<id>` - Obtener miembro específico
- `POST /api/members` - Crear miembro
- `PUT /api/members/<id>` - Actualizar miembro
- `DELETE /api/members/<id>` - Eliminar miembro

#### Préstamos
- `GET /api/loans` - Listar todos los préstamos
- `GET /api/loans/<id>` - Obtener préstamo específico
- `POST /api/loans` - Crear préstamo
- `PUT /api/loans/<id>` - Actualizar préstamo (devolver)
- `DELETE /api/loans/<id>` - Eliminar préstamo

---

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 3.0.0** - Framework web
- **Flask-Marshmallow 1.2.1** - Serialización
- **Marshmallow 3.20.1** - Validación de datos
- **Werkzeug 3.0.0** - Seguridad (hash de contraseñas)

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos
- **Jinja2** - Motor de templates

### Características Técnicas
- **Herencia de templates** con Jinja2
- **Decoradores personalizados** para autenticación
- **Sesiones** de Flask
- **Mensajes flash** para feedback
- **Serialización** con Marshmallow
- **REST API** completa
- **Diseño responsivo** (mobile-first)

---

## 📖 Guía de Uso

### 1. Iniciar Sesión

1. Accede a `http://localhost:5000`
2. Ingresa las credenciales (admin/admin123 o bibliotecario/biblio123)
3. Serás redirigido al dashboard

### 2. Dashboard

El dashboard muestra:
- Total de libros en el catálogo
- Libros disponibles para préstamo
- Miembros activos registrados
- Préstamos activos actualmente

### 3. Gestionar Libros

1. Click en "Libros" en la navegación
2. Completa el formulario para agregar un libro
3. El libro aparecerá en la tabla inferior
4. Usa el botón 🗑️ para eliminar

### 4. Registrar Miembros

1. Click en "Miembros"
2. Completa el formulario de registro
3. El miembro aparecerá en la lista
4. Usa el botón 🗑️ para eliminar

### 5. Crear Préstamos

1. Click en "Préstamos"
2. Selecciona un libro disponible
3. Selecciona un miembro
4. Click en "Registrar Préstamo"
5. El libro se marcará como "Prestado"

### 6. Devolver Libros

1. En la tabla de préstamos, localiza el préstamo activo
2. Click en el botón "✅ Devolver"
3. El libro volverá a estar disponible

### 7. Gestionar Usuarios (Solo Admin)

1. Click en "Usuarios"
2. Completa el formulario para crear un usuario
3. Selecciona el rol (Admin o Bibliotecario)
4. El nuevo usuario podrá iniciar sesión

---

## 🔌 Uso de la API REST

### Autenticación

La API requiere que el usuario esté autenticado. Primero inicia sesión en el navegador.

### Ejemplos con cURL

#### Obtener todos los libros
```bash
curl -X GET http://localhost:5000/api/books
```

#### Crear un libro
```bash
curl -X POST http://localhost:5000/api/books \
  -H "Content-Type: application/json" \
  -d '{
    "titulo": "El Principito",
    "autor": "Antoine de Saint-Exupéry",
    "isbn": "978-0156012195",
    "año_publicacion": 1943,
    "categoria": "Infantil"
  }'
```

#### Crear un miembro
```bash
curl -X POST http://localhost:5000/api/members \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Ana",
    "apellido": "Rodríguez",
    "correo": "ana@email.com",
    "telefono": "787-111-2222"
  }'
```

#### Crear un préstamo
```bash
curl -X POST http://localhost:5000/api/loans \
  -H "Content-Type: application/json" \
  -d '{
    "libro_id": 1,
    "miembro_id": 1
  }'
```

#### Marcar préstamo como devuelto
```bash
curl -X PUT http://localhost:5000/api/loans/1
```

---

## 🎨 Personalización

### Cambiar Colores

Edita `static/css/style.css`:

```css
/* Cambiar gradiente principal */
.header {
    background: linear-gradient(135deg, #TU_COLOR1 0%, #TU_COLOR2 100%);
}
```

### Agregar más Campos

1. Actualiza el esquema en `app.py`
2. Agrega el campo al formulario HTML
3. Actualiza la tabla de visualización

### Cambiar Puerto

En `app.py`, modifica la última línea:

```python
app.run(debug=True, port=5000)  # Cambiar 5000 por el puerto deseado
```

---

## 🛡️ Seguridad

### Características Implementadas

- ✅ **Contraseñas hasheadas** con Werkzeug
- ✅ **Sesiones seguras** con secret key
- ✅ **Protección de rutas** con decoradores
- ✅ **Validación de datos** con Marshmallow
- ✅ **Control de acceso** por roles

### Recomendaciones para Producción

1. **Cambiar la secret key:**
   ```python
   app.secret_key = 'clave_aleatoria_muy_segura_y_larga'
   ```

2. **Usar HTTPS** en lugar de HTTP

3. **Agregar base de datos** (SQLite, PostgreSQL, MySQL)

4. **Implementar rate limiting**

5. **Validación adicional** del lado del servidor

6. **Logs de auditoría** para acciones críticas

---

## 📊 Códigos de Estado HTTP

| Código | Descripción | Uso en la API |
|--------|-------------|---------------|
| 200 | OK | Operación exitosa |
| 201 | Created | Recurso creado |
| 400 | Bad Request | Datos inválidos |
| 404 | Not Found | Recurso no encontrado |
| 302 | Redirect | Redirección (formularios) |

---

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError"

**Causa:** Falta instalar dependencias

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "Address already in use"

**Causa:** El puerto 5000 ya está en uso

**Solución:** Cambiar el puerto en `app.py` o liberar el puerto:
```bash
# En Windows
netstat -ano | findstr :5000
taskkill /PID <número> /F

# En Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Los estilos CSS no se cargan

**Causa:** Estructura de carpetas incorrecta

**Solución:** Verificar que existe `static/css/style.css`

### Error al crear préstamo

**Causa:** El libro no está disponible

**Solución:** Verificar que el libro esté marcado como "Disponible"

---

## 📝 Notas Importantes

### Datos en Memoria

⚠️ **IMPORTANTE:** Los datos se almacenan en memoria y se perderán al reiniciar el servidor.

Para persistencia permanente:
1. Integrar SQLAlchemy
2. Usar base de datos SQLite/PostgreSQL
3. Migrar los datos de las listas a tablas

### Limitaciones Actuales

- Sin paginación en las tablas
- Sin búsqueda/filtros
- Sin edición inline
- Sin persistencia de datos
- Sin sistema de multas
- Sin reservas de libros

---

## 🚀 Mejoras Futuras

### Fase 1: Base de Datos
- [ ] Integrar SQLAlchemy
- [ ] Migración a SQLite
- [ ] Persistencia de datos

### Fase 2: Funcionalidades
- [ ] Sistema de búsqueda
- [ ] Filtros en tablas
- [ ] Paginación
- [ ] Edición de registros
- [ ] Historial de préstamos

### Fase 3: Avanzado
- [ ] Sistema de multas por retraso
- [ ] Reservas de libros
- [ ] Notificaciones por email
- [ ] Reportes en PDF/Excel
- [ ] Dashboard con gráficos
- [ ] Autenticación con JWT
- [ ] OAuth2 (Google, Facebook)

---

## 🎓 Conceptos Aprendidos

Este proyecto demuestra:

- ✅ Creación de REST API con Flask
- ✅ Serialización con Marshmallow
- ✅ Autenticación y hash de contraseñas
- ✅ Autorización basada en roles
- ✅ Templates Jinja2 con herencia
- ✅ Separación de CSS en archivos externos
- ✅ Formularios HTML y validación
- ✅ Manejo de sesiones
- ✅ Mensajes flash
- ✅ Decoradores personalizados
- ✅ Diseño responsivo
- ✅ Buenas prácticas de Flask

---

## 📚 Recursos Adicionales

### Documentación Oficial
- [Flask](https://flask.palletsprojects.com/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [Marshmallow](https://marshmallow.readthedocs.io/)
- [Werkzeug](https://werkzeug.palletsprojects.com/)

### Tutoriales Recomendados
- Flask Mega-Tutorial
- Real Python - Flask
- Python REST APIs with Flask

### Comunidad
- Stack Overflow (tag: flask)
- Reddit: r/flask
- Discord: Flask Community

---

## 👨‍💻 Información del Proyecto

**Nombre:** Sistema Gestor de Biblioteca  
**Tipo:** Proyecto Capstone  
**Curso:** Fundamentos de REST APIs y Serialización  
**Tecnologías:** Flask, Jinja2, Marshmallow, Werkzeug, HTML5, CSS3  
**Fecha:** Diciembre 2024  
**Versión:** 1.0.0

---

## 📄 Licencia

Este proyecto es de uso educativo. Puedes modificarlo y adaptarlo según tus necesidades.

---

## 🙏 Agradecimientos

Gracias por usar el Sistema Gestor de Biblioteca. Si tienes preguntas o sugerencias, no dudes en compartirlas.

---

## 📞 Soporte

Para problemas o preguntas:

1. Revisa la sección "Solución de Problemas"
2. Verifica que todas las dependencias estén instaladas
3. Confirma que la estructura de carpetas sea correcta
4. Revisa los logs en la consola

---

**¡Disfruta gestionando tu biblioteca! 📚✨**