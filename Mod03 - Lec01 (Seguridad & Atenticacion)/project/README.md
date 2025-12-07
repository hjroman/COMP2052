# 🔐 Sistema de Autenticación Flask - Proyecto Capstone

## 📝 Descripción del Proyecto

Sistema completo de autenticación y autorización implementado con Flask y Flask-Login. Este proyecto demuestra las mejores prácticas de seguridad en aplicaciones back-end, incluyendo hashing de contraseñas, gestión de sesiones, y control de acceso basado en roles.

---

## ✨ Características Principales

✅ **Autenticación Segura**
- Login con validación de credenciales
- Contraseñas hasheadas con Werkzeug (PBKDF2-SHA256)
- Gestión automática de sesiones con Flask-Login
- Opción "Recordarme" para sesiones persistentes

✅ **Control de Acceso por Roles**
- Administrador: Acceso completo al sistema
- Moderador: Acceso a herramientas de moderación
- Usuario: Acceso a funciones básicas

✅ **Rutas Protegidas**
- Decorador `@login_required` para proteger rutas
- Verificación de permisos por rol
- Redirección automática a login si no está autenticado

✅ **Interfaz de Usuario**
- Diseño moderno y responsive
- Mensajes flash para retroalimentación
- Navegación intuitiva
- Estilos CSS integrados

---

## 🚀 Instalación y Configuración

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Clonar o Descargar el Proyecto

```bash
# Si usas Git
git clone <url-de-tu-repositorio>
cd proyecto-capstone-autenticacion

# O simplemente descarga los archivos y colócalos en una carpeta
```

### Paso 2: Crear Entorno Virtual (Recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install Flask==3.0.0 Flask-Login==0.6.3 Werkzeug==3.0.1
```

### Paso 4: Ejecutar la Aplicación

```bash
python app.py
```

### Paso 5: Acceder a la Aplicación

Abre tu navegador y visita:
```
http://127.0.0.1:5000
```

---

## 👥 Usuarios de Prueba

El sistema viene con 3 usuarios precargados para probar diferentes niveles de acceso:

| Usuario | Contraseña | Rol | Acceso |
|---------|------------|-----|---------|
| **admin** | admin123 | Administrador | Todas las rutas |
| **moderador** | mod123 | Moderador | Dashboard, Perfil, Moderación |
| **usuario1** | pass123 | Usuario | Dashboard, Perfil |

---

## 🗺️ Estructura de Rutas

### Rutas Públicas

| Ruta | Descripción |
|------|-------------|
| `GET /` | Página de inicio |
| `GET /login` | Formulario de inicio de sesión |
| `POST /login` | Procesar credenciales de login |

### Rutas Protegidas (Requieren Autenticación)

| Ruta | Rol Mínimo | Descripción |
|------|-----------|-------------|
| `GET /dashboard` | Todos | Panel principal del usuario |
| `GET /perfil` | Todos | Ver información del perfil |
| `GET /logout` | Todos | Cerrar sesión |
| `GET /moderacion` | Moderador | Panel de moderación |
| `GET /admin` | Administrador | Panel de administración |

---

## 🔒 Características de Seguridad

### 1. Hashing de Contraseñas
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Las contraseñas se hashean antes de almacenarse
password_hash = generate_password_hash("contraseña")

# Verificación segura sin exponer la contraseña
is_valid = check_password_hash(password_hash, "contraseña")
```

### 2. Gestión de Sesiones
- ID de sesión único por usuario
- Cookie segura con `secret_key`
- Expiración automática de sesiones
- Opción de "Recordarme"

### 3. Protección de Rutas
```python
@app.route("/dashboard")
@login_required  # Solo usuarios autenticados
def dashboard():
    return render_template("dashboard.html")
```

### 4. Control de Acceso por Roles
```python
if current_user.role != "administrador":
    flash("Acceso denegado", "error")
    return redirect(url_for("dashboard"))
```

---

## 📊 Diagrama de Flujo de Autenticación

```
Usuario → Login → Validar Credenciales
                       ↓
                  ¿Válido?
                ↙         ↘
              Sí          No
              ↓           ↓
        Crear Sesión   Mostrar Error
              ↓
         Dashboard
              ↓
      ¿Ruta Protegida?
        ↙         ↘
      Sí          No
      ↓           ↓
¿Tiene Permisos?  Acceso Libre
  ↙         ↘
Sí          No
↓           ↓
Acceso    Denegado
```

---

## 🧪 Probar la Aplicación

### Escenario 1: Login Exitoso
1. Ir a http://127.0.0.1:5000/login
2. Ingresar: `admin` / `admin123`
3. Click en "Ingresar"
4. Deberías ver el Dashboard con mensaje de bienvenida

### Escenario 2: Credenciales Incorrectas
1. Ir a http://127.0.0.1:5000/login
2. Ingresar: `admin` / `contraseña_incorrecta`
3. Deberías ver mensaje de error

### Escenario 3: Acceso a Ruta Protegida sin Login
1. Ir directamente a http://127.0.0.1:5000/dashboard
2. Deberías ser redirigido a /login

### Escenario 4: Control de Permisos
1. Login como `usuario1` / `pass123`
2. Intentar acceder a http://127.0.0.1:5000/admin
3. Deberías ver mensaje de acceso denegado

### Escenario 5: Cerrar Sesión
1. Después de hacer login
2. Click en "Cerrar Sesión"
3. Deberías volver a la página principal

---

## 📁 Estructura de Archivos

```
proyecto-capstone/
│
├── app.py                 # Aplicación Flask principal
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
│
└── (opcional)
    ├── templates/        # Templates HTML separados
    ├── static/          # CSS, JS, imágenes
    └── docs/            # Documentación adicional
```

---

## 🔧 Personalización

### Cambiar la Secret Key
```python
app.secret_key = "tu_clave_secreta_aqui"  # Línea 10 en app.py
```

### Agregar Nuevos Usuarios
```python
users_db["nuevo_usuario"] = User(
    id=4,
    username="nuevo_usuario",
    password_hash=generate_password_hash("contraseña"),
    role="usuario"
)
```

### Crear Nuevos Roles
1. Agregar el rol al crear usuarios
2. Actualizar las verificaciones de permisos en las rutas

---

## 📚 Conceptos Implementados

### Del Documento Original:

✅ **Aspectos de Seguridad**
- Protección contra SQL Injection (ORM pattern)
- Validación de datos de entrada
- Hashing de contraseñas

✅ **Confidencialidad**
- Contraseñas nunca en texto plano
- Sesiones seguras con cookies

✅ **Integridad**
- Validación de credenciales
- Control de acceso por roles

✅ **Disponibilidad**
- Sistema de sesiones robusto
- Manejo de errores apropiado

✅ **Confianza del Usuario**
- Mensajes claros de retroalimentación
- Interfaz intuitiva

---

## 🚨 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'flask'"
```bash
pip install flask flask-login
```

### Error: "Address already in use"
El puerto 5000 está ocupado. Cambia el puerto:
```python
app.run(debug=True, port=5001)
```

### No se guardan las sesiones
Verifica que `app.secret_key` esté configurado correctamente.

---

## 📈 Mejoras Futuras

- [ ] Base de datos real (SQLAlchemy con SQLite/PostgreSQL)
- [ ] Registro de nuevos usuarios
- [ ] Recuperación de contraseña por email
- [ ] Autenticación de dos factores (2FA)
- [ ] API REST con tokens JWT
- [ ] Rate limiting para prevenir brute force
- [ ] Logs de auditoría
- [ ] Tests unitarios y de integración

---

## 📖 Referencias y Recursos

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Werkzeug Security](https://werkzeug.palletsprojects.com/)
- [OWASP Security Guidelines](https://owasp.org/)

---

## 👨‍💻 Autor

Proyecto Capstone - Módulo 03: Seguridad y Autenticación en Aplicaciones Back-End

---

## 📄 Licencia

Este proyecto es material educativo para fines de aprendizaje.

---

## 🤝 Contribuciones

Este es un proyecto educativo. Si encuentras errores o tienes sugerencias:
1. Documenta el problema/sugerencia
2. Crea un issue en el repositorio
3. Propón mejoras mediante pull requests

---

## ✅ Checklist de Entrega

- [x] Servidor Flask con Flask-Login implementado
- [x] Rutas restringidas con `@login_required`
- [x] Sistema de roles y permisos
- [x] Formulario de inicio de sesión funcional
- [x] Hashing de contraseñas con Werkzeug
- [x] Gestión de sesiones
- [x] Cierre de sesión implementado
- [x] Diagrama de flujo de autenticación
- [x] Esquema de usuario documentado
- [x] README con instrucciones completas
- [x] Código comentado y organizado

---

**¡Proyecto completado exitosamente! 🎉**