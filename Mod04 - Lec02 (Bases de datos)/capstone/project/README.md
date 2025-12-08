# 📚 Sistema Gestor de Biblioteca - Proyecto Capstone con MySQL

## 📋 Descripción del Proyecto

Sistema integral de gestión de biblioteca desarrollado con Flask que incluye autenticación, autorización basada en roles, interfaz web completa con templates Jinja2, formularios HTML, REST API y **base de datos MySQL** para persistencia de datos.

**Características principales:**
- ✅ Gestión de libros
- ✅ Gestión de miembros
- ✅ Control de préstamos
- ✅ Sistema de autenticación
- ✅ Roles de usuario (Admin y Bibliotecario)
- ✅ REST API completa
- ✅ **Base de datos MySQL** (datos persistentes)
- ✅ Interfaz moderna y responsiva

---

## 🎯 Nuevo: Integración con Base de Datos

Este proyecto ahora utiliza **MySQL** como base de datos en lugar de almacenar los datos en memoria. 

### Ventajas:
- ✅ **Persistencia permanente** - Los datos no se pierden al reiniciar
- ✅ **Integridad referencial** - Relaciones entre tablas
- ✅ **Consultas SQL** eficientes
- ✅ **Escalabilidad** para múltiples usuarios
- ✅ **Backup y recuperación** de datos

---

## 📁 Estructura del Proyecto

```
biblioteca/
│
├── app.py                      # Aplicación Flask (con integración DB)
├── config.py                   # Configuración de base de datos ⭐
├── database.py                 # Data Layer - capa de datos ⭐
├── database.sql                # Script SQL para crear BD ⭐
├── setup_users.py              # Script para crear usuarios ⭐
├── diagnostico.py              # Script de diagnóstico ⭐
├── requirements.txt            # Dependencias (incluye mysql-connector)
├── README.md                   # Este archivo
│
├── static/
│   └── css/
│       └── style.css          # Estilos CSS
│
└── templates/                  # Templates HTML
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── books.html
    ├── members.html
    ├── loans.html
    └── users.html
```

⭐ = Archivos nuevos para integración con base de datos

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.8 o superior**
- **MySQL Server 8.0 o superior**
- pip (gestor de paquetes de Python)

### Paso 1: Instalar MySQL Server

#### Windows:
1. Descargar desde: https://dev.mysql.com/downloads/mysql/
2. Ejecutar instalador
3. Configurar contraseña para usuario `root`
4. Puerto: `3306` (default)

#### Mac:
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

### Paso 2: Verificar MySQL

```bash
mysql --version
# Debería mostrar: mysql  Ver 8.0.x
```

### Paso 3: Clonar/Descargar el Proyecto

```bash
mkdir biblioteca
cd biblioteca
# Copiar todos los archivos del proyecto aquí
```

### Paso 4: Crear Estructura de Carpetas

```bash
mkdir -p static/css templates
```

### Paso 5: Instalar Dependencias de Python

Crear `requirements.txt`:
```
Flask==3.0.0
flask-marshmallow==1.2.1
marshmallow==3.20.1
Werkzeug==3.0.0
mysql-connector-python==8.2.0
```

Instalar:
```bash
pip install -r requirements.txt
```

### Paso 6: Configurar Conexión a MySQL

Editar `config.py`:

```python
class DatabaseConfig:
    HOST = "localhost"
    USER = "root"
    PASSWORD = "TU_CONTRASEÑA_MYSQL"  # ⚠️ CAMBIAR AQUÍ
    DATABASE = "biblioteca_db"
    PORT = 3306
```

### Paso 7: Crear la Base de Datos

Ejecutar el script SQL:

```bash
# Opción 1: Desde terminal
mysql -u root -p < database.sql

# Opción 2: Desde MySQL Workbench
# Abrir database.sql y ejecutar
```

### Paso 8: ⚠️ IMPORTANTE - Crear Usuarios

```bash
python setup_users.py
```

**Salida esperada:**
```
==================================================
✅ USUARIOS CREADOS EXITOSAMENTE
==================================================

Credenciales de acceso:
  👨‍💼 Admin:
     Usuario: admin
     Contraseña: admin123

  👤 Bibliotecario:
     Usuario: bibliotecario
     Contraseña: biblio123
==================================================
```

### Paso 9: Verificar Instalación

```bash
python diagnostico.py
```

Este script verifica:
- ✅ Conexión a MySQL
- ✅ Usuarios creados correctamente
- ✅ Hashes de contraseñas funcionando
- ✅ Simulación de login

### Paso 10: Ejecutar la Aplicación

```bash
python app.py
```

Acceder a: **http://localhost:5000**

---

## 🔐 Credenciales de Acceso

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `admin123` | Administrador | Acceso completo + gestión de usuarios |
| `bibliotecario` | `biblio123` | Bibliotecario | Gestión de libros, miembros y préstamos |

---

## 🗄️ Estructura de la Base de Datos

### Tabla: usuarios
```sql
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(500) NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    rol ENUM('admin', 'bibliotecario') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: libros
```sql
CREATE TABLE libros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    autor VARCHAR(150) NOT NULL,
    isbn VARCHAR(20) UNIQUE NOT NULL,
    año_publicacion INT NOT NULL,
    categoria VARCHAR(100) NOT NULL,
    disponible BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: miembros
```sql
CREATE TABLE miembros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tabla: prestamos
```sql
CREATE TABLE prestamos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    libro_id INT NOT NULL,
    miembro_id INT NOT NULL,
    fecha_prestamo TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_devolucion TIMESTAMP NULL,
    estado ENUM('Activo', 'Devuelto') DEFAULT 'Activo',
    FOREIGN KEY (libro_id) REFERENCES libros(id) ON DELETE CASCADE,
    FOREIGN KEY (miembro_id) REFERENCES miembros(id) ON DELETE CASCADE
);
```

---

## 🎯 Funcionalidades del Sistema

### 1. Sistema de Autenticación

- **Login seguro** con hash de contraseñas (Werkzeug)
- **Sesiones persistentes**
- **Logout** con limpieza de sesión
- **Protección de rutas** mediante decoradores

### 2. Gestión de Libros

**Funcionalidades:**
- ➕ Agregar nuevos libros
- 📋 Listar todos los libros
- 🗑️ Eliminar libros
- 📊 Ver estado de disponibilidad
- 💾 **Datos guardados en MySQL**

### 3. Gestión de Miembros

**Funcionalidades:**
- ➕ Registrar nuevos miembros
- 📋 Listar todos los miembros
- 🗑️ Eliminar miembros
- 📅 Ver fecha de registro
- 💾 **Datos guardados en MySQL**

### 4. Gestión de Préstamos

**Funcionalidades:**
- ➕ Registrar nuevos préstamos
- 📋 Listar todos los préstamos
- ✅ Marcar como devuelto
- 🗑️ Eliminar préstamos
- 📊 Ver estado (Activo/Devuelto)
- 🔗 **Integridad referencial** con Foreign Keys

### 5. Gestión de Usuarios (Solo Admin)

**Funcionalidades:**
- ➕ Crear nuevos usuarios del sistema
- 📋 Listar usuarios
- 🗑️ Eliminar usuarios
- 🔒 Protección contra auto-eliminación

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

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/books/create` | Crear libro |
| POST | `/books/delete/<id>` | Eliminar libro |
| POST | `/members/create` | Crear miembro |
| POST | `/members/delete/<id>` | Eliminar miembro |
| POST | `/loans/create` | Crear préstamo |
| POST | `/loans/return/<id>` | Devolver libro |
| POST | `/loans/delete/<id>` | Eliminar préstamo |
| POST | `/users/create` | Crear usuario |
| POST | `/users/delete/<id>` | Eliminar usuario |

### REST API (JSON)

#### Libros
- `GET /api/books` - Listar
- `GET /api/books/<id>` - Obtener
- `POST /api/books` - Crear
- `PUT /api/books/<id>` - Actualizar
- `DELETE /api/books/<id>` - Eliminar

#### Miembros
- `GET /api/members` - Listar
- `GET /api/members/<id>` - Obtener
- `POST /api/members` - Crear
- `PUT /api/members/<id>` - Actualizar
- `DELETE /api/members/<id>` - Eliminar

#### Préstamos
- `GET /api/loans` - Listar
- `GET /api/loans/<id>` - Obtener
- `POST /api/loans` - Crear
- `PUT /api/loans/<id>` - Devolver
- `DELETE /api/loans/<id>` - Eliminar

---

## 🔧 Tecnologías Utilizadas

### Backend
- **Flask 3.0.0** - Framework web
- **Flask-Marshmallow 1.2.1** - Serialización
- **Marshmallow 3.20.1** - Validación de datos
- **Werkzeug 3.0.0** - Seguridad (hash de contraseñas)
- **mysql-connector-python 8.2.0** - Conector MySQL ⭐

### Base de Datos
- **MySQL 8.0+** - Sistema de gestión de base de datos ⭐

### Frontend
- **HTML5** - Estructura
- **CSS3** - Estilos
- **Jinja2** - Motor de templates

---

## 🏗️ Arquitectura del Proyecto

### Flujo de Datos

```
[Usuario] 
    ↓
[Templates HTML (Jinja2)]
    ↓
[Flask App (app.py)]
    ↓
[Data Layer (database.py)] ← Abstracción de BD
    ↓
[Config (config.py)] ← Configuración
    ↓
[MySQL Database] ← Persistencia
```

### Data Layer (Capa de Datos)

El archivo `database.py` contiene todos los métodos para interactuar con MySQL:

**Usuarios:**
- `get_user_by_username(username)`
- `get_all_users()`
- `create_user(username, password, nombre, rol)`
- `delete_user(user_id)`

**Libros:**
- `get_all_books()`
- `get_book_by_id(book_id)`
- `create_book(titulo, autor, isbn, año, categoria)`
- `update_book(...)`
- `delete_book(book_id)`
- `update_book_availability(book_id, disponible)`

**Miembros:**
- `get_all_members()`
- `get_member_by_id(member_id)`
- `create_member(nombre, apellido, correo, telefono)`
- `update_member(...)`
- `delete_member(member_id)`

**Préstamos:**
- `get_all_loans()`
- `get_loan_by_id(loan_id)`
- `create_loan(libro_id, miembro_id)`
- `return_loan(loan_id)`
- `delete_loan(loan_id)`

---

## 📖 Guía de Uso

### 1. Iniciar Sesión

1. Ir a `http://localhost:5000`
2. Usar credenciales: `admin` / `admin123`
3. Serás redirigido al dashboard

### 2. Dashboard

Muestra estadísticas en tiempo real desde la base de datos:
- Total de libros
- Libros disponibles
- Miembros activos
- Préstamos activos

### 3. Gestionar Libros

1. Click en "Libros"
2. Completar formulario
3. Los datos se guardan en MySQL
4. Verificar: `SELECT * FROM libros;`

### 4. Crear Préstamos

1. Click en "Préstamos"
2. Seleccionar libro disponible
3. Seleccionar miembro
4. El sistema automáticamente:
   - Crea el préstamo en MySQL
   - Marca el libro como no disponible
   - Registra la fecha

---

## 🧪 Consultas SQL Útiles

### Ver todos los préstamos activos con detalles
```sql
SELECT 
    p.id,
    l.titulo AS libro,
    l.autor,
    CONCAT(m.nombre, ' ', m.apellido) AS miembro,
    p.fecha_prestamo,
    p.estado
FROM prestamos p
JOIN libros l ON p.libro_id = l.id
JOIN miembros m ON p.miembro_id = m.id
WHERE p.estado = 'Activo';
```

### Contar libros por categoría
```sql
SELECT categoria, COUNT(*) as total
FROM libros
GROUP BY categoria;
```

### Libros más prestados
```sql
SELECT 
    l.titulo,
    l.autor,
    COUNT(p.id) as veces_prestado
FROM libros l
LEFT JOIN prestamos p ON l.id = p.libro_id
GROUP BY l.id
ORDER BY veces_prestado DESC
LIMIT 10;
```

### Miembros con préstamos activos
```sql
SELECT 
    CONCAT(m.nombre, ' ', m.apellido) AS miembro,
    COUNT(p.id) as prestamos_activos
FROM miembros m
LEFT JOIN prestamos p ON m.id = p.miembro_id AND p.estado = 'Activo'
GROUP BY m.id
HAVING prestamos_activos > 0;
```

---

## 🐛 Solución de Problemas

### Error: "Can't connect to MySQL server"

**Causa:** MySQL no está corriendo

**Solución:**
```bash
# Windows
net start mysql

# Mac
brew services start mysql

# Linux
sudo systemctl start mysql
```

### Error: "Access denied for user 'root'"

**Causa:** Contraseña incorrecta en `config.py`

**Solución:** Verificar contraseña en `config.py`

### Error: "Unknown database 'biblioteca_db'"

**Causa:** Base de datos no creada

**Solución:**
```bash
mysql -u root -p < database.sql
```

### Error: Login no funciona

**Causa:** Usuarios no creados o hashes incorrectos

**Solución:**
```bash
# 1. Ejecutar diagnóstico
python diagnostico.py

# 2. Crear usuarios correctamente
python setup_users.py
```

### Error: "ModuleNotFoundError: No module named 'mysql'"

**Solución:**
```bash
pip install mysql-connector-python
```

---

## 🔒 Seguridad

### Implementado:
- ✅ Contraseñas hasheadas con Werkzeug
- ✅ Sesiones seguras
- ✅ Protección de rutas
- ✅ Validación de datos con Marshmallow
- ✅ Foreign Keys para integridad referencial

### Recomendaciones para Producción:

1. **Variables de entorno** para credenciales:
```python
import os
DATABASE_PASSWORD = os.getenv('DB_PASSWORD')
```

2. **Usuario específico de MySQL:**
```sql
CREATE USER 'biblioteca_user'@'localhost' IDENTIFIED BY 'password_seguro';
GRANT ALL PRIVILEGES ON biblioteca_db.* TO 'biblioteca_user'@'localhost';
```

3. **Backup automático:**
```bash
mysqldump -u root -p biblioteca_db > backup_$(date +%Y%m%d).sql
```

4. **HTTPS** en producción

5. **.gitignore:**
```
config.py
*.pyc
__pycache__/
venv/
```

---

## 📊 Datos Iniciales

El proyecto incluye datos de ejemplo:

**Libros:**
- Cien Años de Soledad - Gabriel García Márquez
- Don Quijote de la Mancha - Miguel de Cervantes
- 1984 - George Orwell

**Miembros:**
- María González
- Pedro Martínez

**Usuarios del sistema:**
- admin (rol: admin)
- bibliotecario (rol: bibliotecario)

---

## ✅ Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] MySQL instalado y corriendo
- [ ] Base de datos `biblioteca_db` creada
- [ ] Tablas creadas con `database.sql`
- [ ] ⚠️ Usuarios creados con `python setup_users.py`
- [ ] `config.py` configurado
- [ ] Dependencias instaladas (`pip install -r requirements.txt`)
- [ ] Diagnóstico exitoso (`python diagnostico.py`)
- [ ] Aplicación corriendo (`python app.py`)
- [ ] Login funcional con admin/admin123
- [ ] CRUD de libros funcional
- [ ] CRUD de miembros funcional
- [ ] Sistema de préstamos funcional

---

## 🚀 Próximos Pasos

Con la base de datos integrada, puedes agregar:

1. ✅ **Búsqueda y filtros** en las tablas
2. ✅ **Paginación** para grandes volúmenes
3. ✅ **Reportes** con consultas SQL avanzadas
4. ✅ **Historial** completo de préstamos
5. ✅ **Sistema de multas** por retrasos
6. ✅ **Estadísticas** con gráficos
7. ✅ **Notificaciones** por email
8. ✅ **Reservas** de libros
9. ✅ **Exportación** a PDF/Excel
10. ✅ **API REST** con autenticación JWT

---

## 📚 Recursos Adicionales

### Documentación
- [Flask](https://flask.palletsprojects.com/)
- [MySQL](https://dev.mysql.com/doc/)
- [mysql-connector-python](https://dev.mysql.com/doc/connector-python/en/)
- [Jinja2](https://jinja.palletsprojects.com/)
- [Marshmallow](https://marshmallow.readthedocs.io/)

### Tutoriales
- [Python + MySQL](https://www.w3schools.com/python/python_mysql_getstarted.asp)
- [Flask REST API](https://flask-restful.readthedocs.io/)
- [SQL Tutorial](https://www.w3schools.com/sql/)

---

## 👨‍💻 Información del Proyecto

**Nombre:** Sistema Gestor de Biblioteca  
**Tipo:** Proyecto Capstone  
**Curso:** Fundamentos de REST APIs y Serialización  
**Tecnologías:** Flask, MySQL, Jinja2, Marshmallow, Werkzeug  
**Base de Datos:** MySQL 8.0+  
**Fecha:** Diciembre 2024  
**Versión:** 2.0.0 (con MySQL)

---

## 📄 Licencia

Este proyecto es de uso educativo. Puedes modificarlo y adaptarlo según tus necesidades.

---

## 🙏 Agradecimientos

Gracias por usar el Sistema Gestor de Biblioteca con MySQL. 

---

## 📞 Soporte

Para problemas:

1. Ejecutar: `python diagnostico.py`
2. Revisar la sección "Solución de Problemas"
3. Verificar que MySQL esté corriendo
4. Comprobar credenciales en `config.py`
5. Revisar logs en la consola

---

**¡Disfruta gestionando tu biblioteca con persistencia de datos! 📚✨🗄️**