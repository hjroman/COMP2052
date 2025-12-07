from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from flask_principal import Principal, Permission, RoleNeed, identity_loaded, UserNeed, identity_changed, Identity, AnonymousIdentity
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Configuración de la aplicación
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu-clave-secreta-muy-segura-aqui-123456'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///roles_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializar extensiones
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor inicia sesión para acceder a esta página.'
login_manager.login_message_category = 'info'
principal = Principal(app)

# Definir permisos usando Flask-Principal
admin_permission = Permission(RoleNeed('admin'))
editor_permission = Permission(RoleNeed('editor'))
user_permission = Permission(RoleNeed('user'))

# Modelos de la base de datos
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    permissions = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Role {self.name}>'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Configurar identity para Flask-Principal
@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user
    
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))
    
    if hasattr(current_user, 'role') and current_user.role:
        identity.provides.add(RoleNeed(current_user.role.name))

# Diccionario de roles y permisos
roles_permissions = {
    "admin": ["create", "read", "update", "delete"],
    "editor": ["read", "update"],
    "user": ["read"]
}

# Función auxiliar para verificar permisos
def check_permission(role, action):
    return action in roles_permissions.get(role, [])

# Decorador personalizado para verificar permisos
def require_permission(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not permission.can():
                flash('No tienes permisos para acceder a esta página.', 'error')
                return redirect(url_for('dashboard'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Rutas de la aplicación
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Por favor ingresa usuario y contraseña', 'error')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=True)
            # Configurar la identidad para Flask-Principal - CORREGIDO
            identity_changed.send(app, identity=Identity(user.id))
            flash(f'¡Bienvenido {user.username}!', 'success')
            
            # Redirigir a la página siguiente o al dashboard
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'error')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    # Limpiar la identidad - CORREGIDO
    identity_changed.send(app, identity=AnonymousIdentity())
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role:
        user_permissions = roles_permissions.get(current_user.role.name, [])
    else:
        user_permissions = []
    return render_template('dashboard.html', user=current_user, permissions=user_permissions)

# Rutas protegidas por roles
@app.route('/admin')
@login_required
@require_permission(admin_permission)
def admin_panel():
    users = User.query.all()
    return render_template('admin.html', users=users)

@app.route('/editor')
@login_required
@require_permission(editor_permission)
def editor_panel():
    return render_template('editor.html')

@app.route('/user-area')
@login_required
@require_permission(user_permission)
def user_area():
    return render_template('user_area.html')

# API endpoints para pruebas con Postman
@app.route('/api/users', methods=['GET'])
@login_required
def api_get_users():
    if not admin_permission.can():
        return jsonify({'error': 'Acceso denegado'}), 403
    
    users = User.query.all()
    return jsonify({
        'users': [
            {
                'id': user.id,
                'username': user.username,
                #'email': user.email,
                'role': user.role.name if user.role else 'Sin rol'
            } for user in users
        ]
    })

@app.route('/api/create-user', methods=['POST'])
@login_required
def api_create_user():
    if not admin_permission.can():
        return jsonify({'error': 'Acceso denegado'}), 403
    
    data = request.json
    try:
        role = Role.query.get(data['role_id'])
        if not role:
            return jsonify({'error': 'Rol no válido'}), 400
            
        new_user = User(
            username=data['username'],
            email=data['email'],
            role_id=data['role_id']
        )
        new_user.set_password(data['password'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Usuario creado exitosamente'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

# Inicializar la base de datos
def init_db():
    with app.app_context():
        # Eliminar todas las tablas y recrearlas
        db.drop_all()
        db.create_all()
        
        print("Creando roles...")
        # Crear roles
        admin_role = Role(name='admin', permissions='create,read,update,delete')
        editor_role = Role(name='editor', permissions='read,update')
        user_role = Role(name='user', permissions='read')
        
        db.session.add_all([admin_role, editor_role, user_role])
        db.session.commit()
        
        print("Creando usuarios...")
        # Crear usuarios de ejemplo
        admin_user = User(username='admin', email='admin@example.com', role=admin_role)
        admin_user.set_password('admin123')
        
        editor_user = User(username='editor', email='editor@example.com', role=editor_role)
        editor_user.set_password('editor123')
        
        normal_user = User(username='user', email='user@example.com', role=user_role)
        normal_user.set_password('user123')
        
        db.session.add_all([admin_user, editor_user, normal_user])
        db.session.commit()
        
        print("Base de datos inicializada correctamente!")
        print("Usuarios creados:")
        print("- admin / admin123 (Administrador)")
        print("- editor / editor123 (Editor)")  
        print("- user / user123 (Usuario)")

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
