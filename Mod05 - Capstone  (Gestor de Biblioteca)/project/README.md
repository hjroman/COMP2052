# 📚 Sistema Gestor de Biblioteca - Arquitectura de Microservicios

## 🎯 Descripción del Proyecto

Sistema integral de gestión de biblioteca implementado con **arquitectura de microservicios**, que incluye autenticación, autorización basada en roles, base de datos MySQL, y comunicación entre servicios mediante REST API.

**Versión:** 3.0.0 (Microservicios)  
**Tecnologías:** Flask, MySQL, REST API, Microservicios  
**Fecha:** Diciembre 2024

---

## 🏗️ Arquitectura de Microservicios

```
                    ┌─────────────┐
                    │   Usuario   │
                    └──────┬──────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │  API Gateway    │
                  │  (Puerto 5000)  │
                  └────────┬────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
    ┌──────────┐    ┌──────────┐    ┌──────────┐
    │  Auth    │    │  Books   │    │ Members  │
    │ Service  │    │ Service  │    │ Service  │
    │  :5001   │    │  :5002   │    │  :5003   │
    └────┬─────┘    └────┬─────┘    └────┬─────┘
         │               │               │
         │        ┌──────────┐          │
         │        │  Loans   │          │
         │        │ Service  │          │
         │        │  :5004   │          │
         │        └────┬─────┘          │
         │             │                │
         └─────────────┴────────────────┘
                       │
                       ▼
              ┌────────────────┐
              │ MySQL Database │
              │ biblioteca_db  │
              └────────────────┘
```

---

## 🎯 Microservicios Implementados

### 1. **Servicio de Autenticación** (Puerto 5001)
**Responsabilidad:** Gestión de usuarios del sistema y autenticación

**Endpoints:**
- `POST /auth/login` - Autenticar usuario
- `GET /auth/users` - Listar usuarios
- `POST /auth/users` - Crear usuario
- `DELETE /auth/users/<id>` - Eliminar usuario
- `GET /health` - Health check

### 2. **Servicio de Libros** (Puerto 5002)
**Responsabilidad:** Gestión del catálogo de libros

**Endpoints:**
- `GET /books` - Listar todos los libros
- `GET /books/<id>` - Obtener libro específico
- `POST /books` - Crear nuevo libro
- `PUT /books/<id>` - Actualizar libro
- `DELETE /books/<id>` - Eliminar libro
- `PUT /books/<id>/availability` - Actualizar disponibilidad
- `GET /health` - Health check

### 3. **Servicio de Miembros** (Puerto 5003)
**Responsabilidad:** Gestión de miembros de la biblioteca

**Endpoints:**
- `GET /members` - Listar todos los miembros
- `GET /members/<id>` - Obtener miembro específico
- `POST /members` - Crear nuevo miembro
- `PUT /members/<id>` - Actualizar miembro
- `DELETE /members/<id>` - Eliminar miembro
- `GET /health` - Health check

### 4. **Servicio de Préstamos** (Puerto 5004)
**Responsabilidad:** Gestión de préstamos y comunicación entre servicios

**Endpoints:**
- `GET /loans` - Listar todos los préstamos
- `GET /loans/<id>` - Obtener préstamo específico
- `POST /loans` - Crear préstamo (verifica libro y miembro)
- `PUT /loans/<id>/return` - Marcar como devuelto
- `DELETE /loans/<id>` - Eliminar préstamo
- `GET /health` - Health check

**Comunicación entre servicios:**
- Llama a Books Service para verificar disponibilidad
- Llama a Members Service para verificar existencia
- Actualiza disponibilidad del libro automáticamente

### 5. **API Gateway** (Puerto 5000)
**Responsabilidad:** Punto de entrada único, interfaz web y coordinación

**Funciones:**
- Sirve templates HTML (interfaz web)
- Enruta peticiones a microservicios
- Gestiona sesiones de usuario
- Agrega estadísticas del dashboard

---

## 📁 Estructura del Proyecto

```
project/
│
├── services/                        # Microservicios
│   ├── __init__.py
│   ├── auth_service/
│   │   ├── __init__.py
│   │   └── app.py                  # Puerto 5001
│   ├── books_service/
│   │   ├── __init__.py
│   │   └── app.py                  # Puerto 5002
│   ├── members_service/
│   │   ├── __init__.py
│   │   └── app.py                  # Puerto 5003
│   └── loans_service/
│       ├── __init__.py
│       └── app.py                  # Puerto 5004
│
├── gateway/                         # API Gateway
│   └── app.py                      # Puerto 5000
│
├── shared/                          # Código compartido
│   ├── __init__.py
│   ├── config.py                   # Configuración
│   └── database.py                 # Data Layer
│
├── templates/                       # Templates HTML
│   ├── base.html
│   ├── login.html
│   ├── dashboard.html
│   ├── books.html
│   ├── members.html
│   ├── loans.html
│   └── users.html
│
├── static/                          # Archivos estáticos
│   └── css/
│       └── style.css
│
├── start_services.py                # Script para iniciar todo
├── generar_archivos.py             # Script de generación
├── crear_gateway_completo.py       # Script gateway
├── requirements.txt                 # Dependencias
├── database.sql                     # Script SQL
├── setup_users.py                  # Crear usuarios
└── README.md                        # Este archivo
```

---

## 🚀 Instalación y Configuración

### Requisitos Previos

- **Python 3.8+**
- **MySQL 8.0+**
- **pip** (gestor de paquetes)

### Paso 1: Instalar MySQL

#### Windows:
1. Descargar desde: https://dev.mysql.com/downloads/mysql/
2. Instalar y configurar contraseña root
3. Puerto: 3306 (default)

#### Mac:
```bash
brew install mysql
brew services start mysql
```

#### Linux:
```bash
sudo apt install mysql-server
sudo systemctl start mysql
```

### Paso 2: Instalar Dependencias de Python

```bash
pip install -r requirements.txt
```

**Contenido de requirements.txt:**
```
Flask==3.0.0
flask-marshmallow==1.2.1
marshmallow==3.20.1
Werkzeug==3.0.0
mysql-connector-python==8.2.0
requests==2.31.0
```

### Paso 3: Configurar Base de Datos

1. **Crear la base de datos:**
```bash
mysql -u root -p < database.sql
```

2. **Crear usuarios del sistema:**
```bash
python setup_users.py
```

3. **Configurar conexión en `shared/config.py`:**
```python
class DatabaseConfig:
    HOST = "localhost"
    USER = "root"
    PASSWORD = "tu_contraseña"  # ⚠️ CAMBIAR AQUÍ
    DATABASE = "biblioteca_db"
    PORT = 3306
```

### Paso 4: Iniciar los Microservicios

```bash
python start_services.py
```

Esto abrirá **5 ventanas de terminal** (una por cada servicio):
- Auth Service (ventana 1)
- Books Service (ventana 2)
- Members Service (ventana 3)
- Loans Service (ventana 4)
- API Gateway (ventana 5)

### Paso 5: Acceder a la Aplicación

Abre tu navegador en: **http://localhost:5000**

---

## 🔐 Credenciales de Acceso

| Usuario | Contraseña | Rol | Permisos |
|---------|------------|-----|----------|
| `admin` | `admin123` | Administrador | Acceso completo + gestión usuarios |
| `bibliotecario` | `biblio123` | Bibliotecario | Libros, miembros, préstamos |

---

## 🔄 Comunicación Entre Microservicios

### Ejemplo: Crear un Préstamo

**Flujo de comunicación:**

1. Usuario envía formulario → Gateway (puerto 5000)
2. Gateway → Loans Service (puerto 5004)
3. Loans Service → Books Service (puerto 5002)
   - Verifica que el libro existe
   - Verifica que está disponible
4. Loans Service → Members Service (puerto 5003)
   - Verifica que el miembro existe
5. Loans Service → MySQL
   - Crea el préstamo
6. Loans Service → Books Service
   - Actualiza disponibilidad a FALSE
7. Respuesta → Gateway → Usuario

**Código en Loans Service:**
```python
# Verificar libro (comunicación con Books Service)
book_response = requests.get(
    f"{ServiceConfig.BOOKS_SERVICE_URL}/books/{libro_id}"
)

# Verificar miembro (comunicación con Members Service)
member_response = requests.get(
    f"{ServiceConfig.MEMBERS_SERVICE_URL}/members/{miembro_id}"
)

# Crear préstamo
loan_id = DatabaseLayer.create_loan(libro_id, miembro_id)

# Actualizar disponibilidad (comunicación con Books Service)
requests.put(
    f"{ServiceConfig.BOOKS_SERVICE_URL}/books/{libro_id}/availability",
    json={"disponible": False}
)
```

---

## 🧪 Probar los Microservicios

### Health Checks

Verificar que todos los servicios están activos:

```bash
curl http://localhost:5001/health  # Auth
curl http://localhost:5002/health  # Books
curl http://localhost:5003/health  # Members
curl http://localhost:5004/health  # Loans
```

### Probar API directamente

**Obtener libros (Books Service):**
```bash
curl http://localhost:5002/books
```

**Crear préstamo (Loans Service con comunicación):**
```bash
curl -X POST http://localhost:5004/loans \
  -H "Content-Type: application/json" \
  -d '{"libro_id": 1, "miembro_id": 1}'
```

---

## 📊 Base de Datos

### Tablas Implementadas

**usuarios**
- id, username, password, nombre, rol, created_at

**libros**
- id, titulo, autor, isbn, año_publicacion, categoria, disponible, created_at

**miembros**
- id, nombre, apellido, correo, telefono, fecha_registro

**prestamos**
- id, libro_id (FK), miembro_id (FK), fecha_prestamo, fecha_devolucion, estado

### Foreign Keys

- `prestamos.libro_id` → `libros.id` (CASCADE)
- `prestamos.miembro_id` → `miembros.id` (CASCADE)

---

## ✅ Ventajas de la Arquitectura de Microservicios

### 1. **Escalabilidad Independiente**
```bash
# Escalar solo el servicio de libros si tiene mucha demanda
python services/books_service/app.py --port 5012
python services/books_service/app.py --port 5013
# + Load balancer
```

### 2. **Desarrollo Paralelo**
Equipos diferentes pueden trabajar en servicios diferentes sin conflictos.

### 3. **Despliegue Independiente**
Actualizar un servicio sin afectar a los demás:
```bash
# Solo actualizar Books Service
git pull origin main -- services/books_service/
python services/books_service/app.py
```

### 4. **Aislamiento de Fallos**
```
❌ Books Service DOWN
✅ Auth Service OK → Login funciona
✅ Members Service OK → Registro de miembros funciona
✅ Loans Service → Puede devolver préstamos existentes
```

### 5. **Tecnologías Mixtas** (futuro)
Cada servicio puede usar diferentes tecnologías:
```
Auth Service → Python + Flask
Books Service → Node.js + Express
Members Service → Go + Gin
Loans Service → Python + FastAPI
```

---

## 🛑 Detener los Servicios

Para detener todos los servicios:

1. Presiona **Ctrl+C** en la terminal principal
2. **Cierra manualmente las 5 ventanas** que se abrieron

O simplemente cierra todas las ventanas de terminal.

---

## 🐛 Solución de Problemas

### Error: "Unable to connect to localhost:5000"

**Causa:** El Gateway no está corriendo

**Solución:**
```bash
# Verificar que todas las 5 ventanas están abiertas
# Ejecutar de nuevo
python start_services.py
```

### Error: "Connection refused" al crear préstamo

**Causa:** Algún microservicio no está corriendo

**Solución:**
```bash
# Verificar health checks
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
curl http://localhost:5004/health
```

### Error: "ModuleNotFoundError: No module named 'requests'"

**Solución:**
```bash
pip install requests
```

### Error al conectar a MySQL

**Causa:** Contraseña incorrecta en `shared/config.py`

**Solución:** Editar `shared/config.py` con la contraseña correcta

---

## 📖 Guía de Uso

### 1. Iniciar el Sistema
```bash
python start_services.py
```
Se abrirán 5 ventanas (una por servicio)

### 2. Acceder
Abrir navegador en: http://localhost:5000

### 3. Login
- Admin: `admin` / `admin123`
- Bibliotecario: `bibliotecario` / `biblio123`

### 4. Usar la Aplicación
- **Dashboard:** Ver estadísticas
- **Libros:** Agregar, listar, eliminar
- **Miembros:** Registrar, listar, eliminar
- **Préstamos:** Crear, devolver, listar
- **Usuarios:** (Solo admin) Crear, eliminar

### 5. Detener
Cerrar las 5 ventanas de terminal

---

## 🔒 Seguridad

### Implementado:
- ✅ Contraseñas hasheadas (Werkzeug)
- ✅ Sesiones seguras (Flask Session)
- ✅ Protección de rutas por rol
- ✅ Validación de datos (Marshmallow)
- ✅ Foreign Keys (integridad referencial)

### Recomendaciones para Producción:
1. **Variables de entorno** para credenciales
2. **HTTPS** en lugar de HTTP
3. **JWT** para autenticación entre servicios
4. **Rate limiting**
5. **API Gateway** profesional (Kong, Nginx)
6. **Logs centralizados** (ELK Stack)
7. **Monitoreo** (Prometheus, Grafana)
8. **Containerización** (Docker)
9. **Orquestación** (Kubernetes)

---

## 🚀 Próximas Mejoras

### Funcionalidades:
- [ ] Búsqueda y filtros
- [ ] Paginación
- [ ] Sistema de multas
- [ ] Reservas de libros
- [ ] Historial de préstamos
- [ ] Notificaciones por email
- [ ] Exportación a PDF/Excel
- [ ] Reportes avanzados

### Arquitectura:
- [ ] Service Discovery (Consul, Eureka)
- [ ] Circuit Breaker (Hystrix)
- [ ] Message Queue (RabbitMQ, Kafka)
- [ ] Distributed Tracing (Jaeger, Zipkin)
- [ ] Centralized Configuration (Spring Cloud Config)
- [ ] API Gateway avanzado (Kong)
- [ ] Container Orchestration (Kubernetes)

---

## 📚 Recursos de Aprendizaje

### Documentación:
- [Flask](https://flask.palletsprojects.com/)
- [Microservicios - Martin Fowler](https://martinfowler.com/articles/microservices.html)
- [REST API Design](https://restfulapi.net/)
- [MySQL](https://dev.mysql.com/doc/)

### Tutoriales:
- [Microservices with Flask](https://testdriven.io/blog/flask-microservices-development/)
- [Building Microservices](https://www.nginx.com/blog/building-microservices/)

---

## 🎓 Conceptos Aprendidos

Este proyecto demuestra:

✅ **Arquitectura de Microservicios**  
✅ **Comunicación HTTP entre servicios**  
✅ **API Gateway pattern**  
✅ **Service-to-service communication**  
✅ **Separación de responsabilidades**  
✅ **REST API design**  
✅ **Base de datos relacional**  
✅ **Autenticación y autorización**  
✅ **Manejo de sesiones**  
✅ **Escalabilidad horizontal**

---

## 📊 Comparación: Monolito vs Microservicios

| Aspecto | Monolito | Microservicios |
|---------|----------|----------------|
| **Estructura** | Una aplicación | Múltiples servicios |
| **Despliegue** | Todo junto | Independiente |
| **Escalabilidad** | Vertical | Horizontal |
| **Tecnología** | Una sola | Puede variar |
| **Complejidad** | Menor | Mayor |
| **Mantenimiento** | Más difícil a largo plazo | Más fácil |
| **Equipo** | Todos en todo | Por servicio |
| **Fallos** | Afecta todo | Aislados |
| **Desarrollo** | Más lento con el tiempo | Paralelo |

---

## 👨‍💻 Información del Proyecto

**Nombre:** Sistema Gestor de Biblioteca  
**Arquitectura:** Microservicios  
**Tipo:** Proyecto Capstone  
**Curso:** Fundamentos de Microservicios  
**Tecnologías:** Flask, MySQL, REST API, Requests  
**Fecha:** Diciembre 2024  
**Versión:** 3.0.0

---

## 📞 Soporte

### Para problemas:

1. Ejecutar health checks de cada servicio
2. Verificar que MySQL está corriendo
3. Revisar que las 5 ventanas están abiertas
4. Verificar logs en las ventanas de cada servicio
5. Comprobar credenciales en `shared/config.py`

---

## 📄 Licencia

Este proyecto es de uso educativo.

---

**¡Disfruta de tu arquitectura de microservicios! 🚀📚✨**