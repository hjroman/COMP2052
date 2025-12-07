from flask import Flask, render_template_string, request, redirect, url_for, flash, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.secret_key = "clave_secreta_super_segura_2024"

# Configuración de Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Por favor inicia sesión para acceder a esta página."

# Modelo de Usuario
class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Base de datos simulada de usuarios
users_db = {
    "admin": User(
        1, 
        "admin", 
        generate_password_hash("admin123"),
        "administrador"
    ),
    "usuario1": User(
        2, 
        "usuario1", 
        generate_password_hash("pass123"),
        "usuario"
    ),
    "moderador": User(
        3, 
        "moderador", 
        generate_password_hash("mod123"),
        "moderador"
    )
}

@login_manager.user_loader
def load_user(user_id):
    """Callback requerido por Flask-Login para cargar usuario"""
    for user in users_db.values():
        if str(user.id) == user_id:
            return user
    return None

@app.route("/")
def home():
    """Página principal"""
    return render_template_string(HOME_TEMPLATE)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Ruta de inicio de sesión"""
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        remember = request.form.get("remember", False)
        
        user = users_db.get(username)
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            session["login_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            flash(f"¡Bienvenido {user.username}!", "success")
            
            # Redirigir a la página solicitada o al dashboard
            next_page = request.args.get("next")
            return redirect(next_page or url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos", "error")
    
    return render_template_string(LOGIN_TEMPLATE)

@app.route("/logout")
@login_required
def logout():
    """Ruta de cierre de sesión"""
    username = current_user.username
    logout_user()
    session.pop("login_time", None)
    flash(f"Sesión cerrada correctamente. ¡Hasta pronto {username}!", "info")
    return redirect(url_for("home"))

@app.route("/dashboard")
@login_required
def dashboard():
    """Panel principal - Ruta protegida"""
    login_time = session.get("login_time", "N/A")
    return render_template_string(DASHBOARD_TEMPLATE, login_time=login_time)

@app.route("/perfil")
@login_required
def perfil():
    """Perfil de usuario - Ruta protegida"""
    return render_template_string(PERFIL_TEMPLATE)

@app.route("/admin")
@login_required
def admin():
    """Panel de administración - Ruta protegida solo para admin"""
    if current_user.role != "administrador":
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for("dashboard"))
    
    return render_template_string(ADMIN_TEMPLATE, users=users_db)

@app.route("/moderacion")
@login_required
def moderacion():
    """Panel de moderación - Para admin y moderadores"""
    if current_user.role not in ["administrador", "moderador"]:
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for("dashboard"))
    
    return render_template_string(MODERACION_TEMPLATE)

# Templates HTML
HOME_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Autenticación</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 500px; width: 90%; text-align: center; }
        h1 { color: #333; margin-bottom: 10px; }
        p { color: #666; margin-bottom: 30px; line-height: 1.6; }
        .btn { display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 25px; transition: all 0.3s; margin: 5px; }
        .btn:hover { background: #764ba2; transform: translateY(-2px); }
        .features { text-align: left; margin: 30px 0; }
        .features li { margin: 10px 0; color: #555; }
        .lock-icon { font-size: 60px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="lock-icon">🔐</div>
        <h1>Sistema de Autenticación Flask</h1>
        <p>Bienvenido al sistema de gestión de usuarios con Flask-Login</p>
        
        <ul class="features">
            <li>✓ Autenticación segura con hashing</li>
            <li>✓ Gestión de sesiones</li>
            <li>✓ Rutas protegidas</li>
            <li>✓ Roles y permisos</li>
        </ul>
        
        <a href="{{ url_for('login') }}" class="btn">Iniciar Sesión</a>
    </div>
</body>
</html>
"""

LOGIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .container { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 40px rgba(0,0,0,0.2); max-width: 400px; width: 90%; }
        h2 { color: #333; margin-bottom: 30px; text-align: center; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; color: #555; font-weight: 500; }
        input[type="text"], input[type="password"] { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 14px; transition: border 0.3s; }
        input:focus { outline: none; border-color: #667eea; }
        .checkbox-group { display: flex; align-items: center; margin-bottom: 20px; }
        .checkbox-group input { margin-right: 8px; }
        .btn { width: 100%; padding: 12px; background: #667eea; color: white; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; transition: background 0.3s; }
        .btn:hover { background: #764ba2; }
        .alert { padding: 10px; border-radius: 5px; margin-bottom: 20px; }
        .alert-error { background: #fee; color: #c33; border: 1px solid #fcc; }
        .alert-success { background: #efe; color: #3c3; border: 1px solid #cfc; }
        .users-info { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-top: 20px; font-size: 13px; }
        .users-info h4 { margin-bottom: 10px; color: #333; }
        .users-info p { margin: 5px 0; color: #666; }
        .back-link { display: block; text-align: center; margin-top: 15px; color: #667eea; text-decoration: none; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🔐 Iniciar Sesión</h2>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        <form method="POST">
            <div class="form-group">
                <label for="username">Usuario:</label>
                <input type="text" id="username" name="username" required>
            </div>
            
            <div class="form-group">
                <label for="password">Contraseña:</label>
                <input type="password" id="password" name="password" required>
            </div>
            
            <div class="checkbox-group">
                <input type="checkbox" id="remember" name="remember">
                <label for="remember" style="margin-bottom: 0;">Recordarme</label>
            </div>
            
            <button type="submit" class="btn">Ingresar</button>
        </form>
        
        <div class="users-info">
            <h4>👥 Usuarios de Prueba:</h4>
            <p><strong>admin</strong> / admin123 (Administrador)</p>
            <p><strong>usuario1</strong> / pass123 (Usuario)</p>
            <p><strong>moderador</strong> / mod123 (Moderador)</p>
        </div>
        
        <a href="{{ url_for('home') }}" class="back-link">← Volver al inicio</a>
    </div>
</body>
</html>
"""

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { font-size: 24px; }
        .navbar a { color: white; text-decoration: none; margin-left: 20px; padding: 8px 16px; border-radius: 5px; transition: background 0.3s; }
        .navbar a:hover { background: rgba(255,255,255,0.2); }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        .welcome-card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); margin-bottom: 30px; }
        .welcome-card h2 { color: #333; margin-bottom: 10px; }
        .user-badge { display: inline-block; padding: 5px 15px; background: #667eea; color: white; border-radius: 15px; font-size: 14px; margin-left: 10px; }
        .cards-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 20px; margin-top: 30px; }
        .card { background: white; padding: 25px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .card:hover { transform: translateY(-5px); }
        .card h3 { color: #667eea; margin-bottom: 15px; }
        .card p { color: #666; line-height: 1.6; }
        .info-item { margin: 10px 0; padding: 10px; background: #f8f9fa; border-radius: 5px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>📊 Dashboard</h1>
        <div>
            <a href="{{ url_for('perfil') }}">Perfil</a>
            {% if current_user.role == 'administrador' %}
            <a href="{{ url_for('admin') }}">Admin</a>
            {% endif %}
            {% if current_user.role in ['administrador', 'moderador'] %}
            <a href="{{ url_for('moderacion') }}">Moderación</a>
            {% endif %}
            <a href="{{ url_for('logout') }}">Cerrar Sesión</a>
        </div>
    </nav>
    
    <div class="container">
        <div class="welcome-card">
            <h2>¡Bienvenido, {{ current_user.username }}! <span class="user-badge">{{ current_user.role }}</span></h2>
            <p style="color: #666; margin-top: 10px;">Has iniciado sesión correctamente. Este es tu panel de control personal.</p>
            <div class="info-item">
                <strong>Hora de inicio de sesión:</strong> {{ login_time }}
            </div>
        </div>
        
        <div class="cards-grid">
            <div class="card">
                <h3>👤 Tu Perfil</h3>
                <p>Visualiza y gestiona tu información personal, configuración de cuenta y preferencias.</p>
            </div>
            
            <div class="card">
                <h3>🔒 Seguridad</h3>
                <p>Tu sesión está protegida con autenticación segura y hashing de contraseñas.</p>
            </div>
            
            <div class="card">
                <h3>📈 Actividad</h3>
                <p>Monitorea tu actividad reciente y accede a tu historial de sesiones.</p>
            </div>
            
            {% if current_user.role == 'administrador' %}
            <div class="card">
                <h3>⚙️ Administración</h3>
                <p>Accede al panel de administración para gestionar usuarios y permisos del sistema.</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
"""

PERFIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Perfil</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { font-size: 24px; }
        .navbar a { color: white; text-decoration: none; margin-left: 20px; padding: 8px 16px; border-radius: 5px; transition: background 0.3s; }
        .navbar a:hover { background: rgba(255,255,255,0.2); }
        .container { max-width: 800px; margin: 40px auto; padding: 0 20px; }
        .profile-card { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        .profile-header { text-align: center; margin-bottom: 30px; }
        .avatar { width: 100px; height: 100px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 48px; margin: 0 auto 15px; }
        .info-section { margin: 20px 0; }
        .info-row { display: flex; padding: 15px; background: #f8f9fa; border-radius: 5px; margin: 10px 0; }
        .info-label { font-weight: 600; color: #555; width: 150px; }
        .info-value { color: #333; }
        .role-badge { display: inline-block; padding: 5px 15px; background: #667eea; color: white; border-radius: 15px; font-size: 14px; }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>👤 Mi Perfil</h1>
        <div>
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('logout') }}">Cerrar Sesión</a>
        </div>
    </nav>
    
    <div class="container">
        <div class="profile-card">
            <div class="profile-header">
                <div class="avatar">👤</div>
                <h2>{{ current_user.username }}</h2>
            </div>
            
            <div class="info-section">
                <h3 style="color: #667eea; margin-bottom: 15px;">Información de la Cuenta</h3>
                
                <div class="info-row">
                    <div class="info-label">ID de Usuario:</div>
                    <div class="info-value">{{ current_user.id }}</div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">Nombre de Usuario:</div>
                    <div class="info-value">{{ current_user.username }}</div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">Rol:</div>
                    <div class="info-value"><span class="role-badge">{{ current_user.role }}</span></div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">Estado:</div>
                    <div class="info-value">✓ Activo</div>
                </div>
                
                <div class="info-row">
                    <div class="info-label">Autenticado:</div>
                    <div class="info-value">{{ "Sí" if current_user.is_authenticated else "No" }}</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

ADMIN_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Administración</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { font-size: 24px; }
        .navbar a { color: white; text-decoration: none; margin-left: 20px; padding: 8px 16px; border-radius: 5px; transition: background 0.3s; }
        .navbar a:hover { background: rgba(255,255,255,0.2); }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        .admin-card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background: #667eea; color: white; }
        tr:hover { background: #f8f9fa; }
        .role-badge { display: inline-block; padding: 5px 10px; border-radius: 12px; font-size: 12px; }
        .role-administrador { background: #dc3545; color: white; }
        .role-moderador { background: #ffc107; color: #333; }
        .role-usuario { background: #28a745; color: white; }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>⚙️ Panel de Administración</h1>
        <div>
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('logout') }}">Cerrar Sesión</a>
        </div>
    </nav>
    
    <div class="container">
        <div class="admin-card">
            <h2 style="color: #333; margin-bottom: 10px;">Gestión de Usuarios</h2>
            <p style="color: #666; margin-bottom: 20px;">Vista completa de todos los usuarios del sistema</p>
            
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Usuario</th>
                        <th>Rol</th>
                        <th>Estado</th>
                    </tr>
                </thead>
                <tbody>
                    {% for username, user in users.items() %}
                    <tr>
                        <td>{{ user.id }}</td>
                        <td>{{ user.username }}</td>
                        <td><span class="role-badge role-{{ user.role }}">{{ user.role }}</span></td>
                        <td>✓ Activo</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>
"""

MODERACION_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Panel de Moderación</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f5f5; }
        .navbar { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .navbar h1 { font-size: 24px; }
        .navbar a { color: white; text-decoration: none; margin-left: 20px; padding: 8px 16px; border-radius: 5px; transition: background 0.3s; }
        .navbar a:hover { background: rgba(255,255,255,0.2); }
        .container { max-width: 1200px; margin: 40px auto; padding: 0 20px; }
        .mod-card { background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    </style>
</head>
<body>
    <nav class="navbar">
        <h1>🛡️ Panel de Moderación</h1>
        <div>
            <a href="{{ url_for('dashboard') }}">Dashboard</a>
            <a href="{{ url_for('logout') }}">Cerrar Sesión</a>
        </div>
    </nav>
    
    <div class="container">
        <div class="mod-card">
            <h2 style="color: #333; margin-bottom: 10px;">Herramientas de Moderación</h2>
            <p style="color: #666;">Panel exclusivo para moderadores y administradores</p>
            <p style="color: #667eea; margin-top: 20px;">Tu rol: <strong>{{ current_user.role }}</strong></p>
        </div>
    </div>
</body>
</html>
"""

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Servidor Flask con Autenticación Iniciado")
    print("=" * 50)
    print("\n📝 Usuarios disponibles:")
    print("   • admin / admin123 (Administrador)")
    print("   • usuario1 / pass123 (Usuario)")
    print("   • moderador / mod123 (Moderador)")
    print("\n🌐 Accede a: http://127.0.0.1:5000")
    print("=" * 50 + "\n")
    app.run(debug=True)