from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_super_segura_123'
ma = Marshmallow(app)

# ==================== DECORADORES DE AUTENTICACIÓN ====================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión', 'warning')
            return redirect(url_for('login'))
        usuario = next((u for u in usuarios if u["id"] == session['user_id']), None)
        if not usuario or usuario['rol'] != 'admin':
            flash('No tienes permisos para acceder a esta página', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# ==================== ESQUEMAS DE SERIALIZACIÓN ====================

class BookSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    titulo = fields.Str(required=True)
    autor = fields.Str(required=True)
    isbn = fields.Str(required=True)
    año_publicacion = fields.Int(required=True)
    categoria = fields.Str(required=True)
    disponible = fields.Bool(dump_only=True)

class MemberSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    nombre = fields.Str(required=True)
    apellido = fields.Str(required=True)
    correo = fields.Email(required=True)
    telefono = fields.Str(required=True)
    fecha_registro = fields.DateTime(dump_only=True)

class LoanSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    libro_id = fields.Int(required=True)
    miembro_id = fields.Int(required=True)
    fecha_prestamo = fields.DateTime(dump_only=True)
    fecha_devolucion = fields.DateTime(allow_none=True)
    estado = fields.Str(dump_only=True)

book_schema = BookSchema()
books_schema = BookSchema(many=True)
member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
loan_schema = LoanSchema()
loans_schema = LoanSchema(many=True)

# ==================== DATOS DE EJEMPLO ====================

usuarios = [
    {
        "id": 1,
        "username": "admin",
        "password": generate_password_hash("admin123"),
        "nombre": "Administrador",
        "rol": "admin"
    },
    {
        "id": 2,
        "username": "bibliotecario",
        "password": generate_password_hash("biblio123"),
        "nombre": "Juan Bibliotecario",
        "rol": "bibliotecario"
    }
]

libros = [
    {
        "id": 1,
        "titulo": "Cien Años de Soledad",
        "autor": "Gabriel García Márquez",
        "isbn": "978-0307474728",
        "año_publicacion": 1967,
        "categoria": "Ficción",
        "disponible": True
    },
    {
        "id": 2,
        "titulo": "Don Quijote de la Mancha",
        "autor": "Miguel de Cervantes",
        "isbn": "978-8420412146",
        "año_publicacion": 1605,
        "categoria": "Clásico",
        "disponible": True
    },
    {
        "id": 3,
        "titulo": "1984",
        "autor": "George Orwell",
        "isbn": "978-0451524935",
        "año_publicacion": 1949,
        "categoria": "Distopía",
        "disponible": True
    }
]

miembros = [
    {
        "id": 1,
        "nombre": "María",
        "apellido": "González",
        "correo": "maria.gonzalez@email.com",
        "telefono": "787-123-4567",
        "fecha_registro": datetime.now()
    },
    {
        "id": 2,
        "nombre": "Pedro",
        "apellido": "Martínez",
        "correo": "pedro.martinez@email.com",
        "telefono": "787-987-6543",
        "fecha_registro": datetime.now()
    }
]

prestamos = []

# ==================== RUTAS DE AUTENTICACIÓN ====================

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        usuario = next((u for u in usuarios if u['username'] == username), None)
        
        if usuario and check_password_hash(usuario['password'], password):
            session['user_id'] = usuario['id']
            session['user_nombre'] = usuario['nombre']
            session['user_rol'] = usuario['rol']
            flash('¡Bienvenido de nuevo!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Usuario o contraseña incorrectos', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    stats = {
        'total_libros': len(libros),
        'libros_disponibles': sum(1 for l in libros if l['disponible']),
        'total_miembros': len(miembros),
        'prestamos_activos': sum(1 for p in prestamos if p['estado'] == 'Activo')
    }
    return render_template('dashboard.html', **stats)

# ==================== RUTAS DE PÁGINAS CON FORMULARIOS ====================

@app.route('/books')
@login_required
def books_page():
    return render_template('books.html', libros=libros)

@app.route('/members')
@login_required
def members_page():
    return render_template('members.html', miembros=miembros)

@app.route('/loans')
@login_required
def loans_page():
    return render_template('loans.html', prestamos=prestamos, libros=libros, miembros=miembros)

@app.route('/users')
@admin_required
def users_page():
    return render_template('users.html', usuarios=usuarios)

# ==================== RUTAS DE FORMULARIOS - LIBROS ====================

@app.route('/books/create', methods=['POST'])
@login_required
def create_book_form():
    try:
        nuevo_libro = {
            "id": max([l['id'] for l in libros], default=0) + 1,
            "titulo": request.form.get('titulo'),
            "autor": request.form.get('autor'),
            "isbn": request.form.get('isbn'),
            "año_publicacion": int(request.form.get('año_publicacion')),
            "categoria": request.form.get('categoria'),
            "disponible": True
        }
        libros.append(nuevo_libro)
        flash(f'Libro "{nuevo_libro["titulo"]}" agregado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear libro: {str(e)}', 'danger')
    return redirect(url_for('books_page'))

@app.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book_form(book_id):
    global libros
    libro = next((l for l in libros if l['id'] == book_id), None)
    if libro:
        libros = [l for l in libros if l['id'] != book_id]
        flash(f'Libro "{libro["titulo"]}" eliminado exitosamente', 'success')
    else:
        flash('Libro no encontrado', 'danger')
    return redirect(url_for('books_page'))

# ==================== RUTAS DE FORMULARIOS - MIEMBROS ====================

@app.route('/members/create', methods=['POST'])
@login_required
def create_member_form():
    try:
        nuevo_miembro = {
            "id": max([m['id'] for m in miembros], default=0) + 1,
            "nombre": request.form.get('nombre'),
            "apellido": request.form.get('apellido'),
            "correo": request.form.get('correo'),
            "telefono": request.form.get('telefono'),
            "fecha_registro": datetime.now()
        }
        miembros.append(nuevo_miembro)
        flash(f'Miembro "{nuevo_miembro["nombre"]} {nuevo_miembro["apellido"]}" registrado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al registrar miembro: {str(e)}', 'danger')
    return redirect(url_for('members_page'))

@app.route('/members/delete/<int:member_id>', methods=['POST'])
@login_required
def delete_member_form(member_id):
    global miembros
    miembro = next((m for m in miembros if m['id'] == member_id), None)
    if miembro:
        miembros = [m for m in miembros if m['id'] != member_id]
        flash(f'Miembro "{miembro["nombre"]} {miembro["apellido"]}" eliminado exitosamente', 'success')
    else:
        flash('Miembro no encontrado', 'danger')
    return redirect(url_for('members_page'))

# ==================== RUTAS DE FORMULARIOS - PRÉSTAMOS ====================

@app.route('/loans/create', methods=['POST'])
@login_required
def create_loan_form():
    try:
        libro_id = int(request.form.get('libro_id'))
        miembro_id = int(request.form.get('miembro_id'))
        
        libro = next((l for l in libros if l['id'] == libro_id), None)
        miembro = next((m for m in miembros if m['id'] == miembro_id), None)
        
        if not libro:
            flash('Libro no encontrado', 'danger')
            return redirect(url_for('loans_page'))
        
        if not miembro:
            flash('Miembro no encontrado', 'danger')
            return redirect(url_for('loans_page'))
        
        if not libro['disponible']:
            flash('El libro no está disponible', 'warning')
            return redirect(url_for('loans_page'))
        
        nuevo_prestamo = {
            "id": max([p['id'] for p in prestamos], default=0) + 1,
            "libro_id": libro_id,
            "miembro_id": miembro_id,
            "fecha_prestamo": datetime.now(),
            "fecha_devolucion": None,
            "estado": "Activo"
        }
        prestamos.append(nuevo_prestamo)
        libro['disponible'] = False
        
        flash(f'Préstamo registrado: "{libro["titulo"]}" para {miembro["nombre"]} {miembro["apellido"]}', 'success')
    except Exception as e:
        flash(f'Error al crear préstamo: {str(e)}', 'danger')
    return redirect(url_for('loans_page'))

@app.route('/loans/return/<int:loan_id>', methods=['POST'])
@login_required
def return_loan_form(loan_id):
    prestamo = next((p for p in prestamos if p['id'] == loan_id), None)
    if prestamo:
        prestamo['fecha_devolucion'] = datetime.now()
        prestamo['estado'] = 'Devuelto'
        
        libro = next((l for l in libros if l['id'] == prestamo['libro_id']), None)
        if libro:
            libro['disponible'] = True
        
        flash('Libro devuelto exitosamente', 'success')
    else:
        flash('Préstamo no encontrado', 'danger')
    return redirect(url_for('loans_page'))

@app.route('/loans/delete/<int:loan_id>', methods=['POST'])
@login_required
def delete_loan_form(loan_id):
    global prestamos
    prestamo = next((p for p in prestamos if p['id'] == loan_id), None)
    if prestamo:
        prestamos = [p for p in prestamos if p['id'] != loan_id]
        flash('Préstamo eliminado exitosamente', 'success')
    else:
        flash('Préstamo no encontrado', 'danger')
    return redirect(url_for('loans_page'))

# ==================== RUTAS DE FORMULARIOS - USUARIOS ====================

@app.route('/users/create', methods=['POST'])
@admin_required
def create_user_form():
    try:
        nuevo_usuario = {
            "id": max([u['id'] for u in usuarios], default=0) + 1,
            "username": request.form.get('username'),
            "password": generate_password_hash(request.form.get('password')),
            "nombre": request.form.get('nombre'),
            "rol": request.form.get('rol')
        }
        usuarios.append(nuevo_usuario)
        flash(f'Usuario "{nuevo_usuario["username"]}" creado exitosamente', 'success')
    except Exception as e:
        flash(f'Error al crear usuario: {str(e)}', 'danger')
    return redirect(url_for('users_page'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user_form(user_id):
    global usuarios
    usuario = next((u for u in usuarios if u['id'] == user_id), None)
    if usuario:
        if usuario['id'] == session['user_id']:
            flash('No puedes eliminar tu propio usuario', 'danger')
        else:
            usuarios = [u for u in usuarios if u['id'] != user_id]
            flash(f'Usuario "{usuario["username"]}" eliminado exitosamente', 'success')
    else:
        flash('Usuario no encontrado', 'danger')
    return redirect(url_for('users_page'))

# ==================== REST API ENDPOINTS (JSON) ====================

@app.route("/api/books", methods=["GET"])
@login_required
def get_books():
    return books_schema.jsonify(libros), 200

@app.route("/api/books/<int:book_id>", methods=["GET"])
@login_required
def get_book(book_id):
    libro = next((l for l in libros if l["id"] == book_id), None)
    if libro:
        return book_schema.jsonify(libro), 200
    return {"error": "Libro no encontrado"}, 404

@app.route("/api/books", methods=["POST"])
@login_required
def create_book():
    try:
        data = request.json
        errors = book_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        
        nuevo_libro = {
            "id": max([l['id'] for l in libros], default=0) + 1,
            "titulo": data["titulo"],
            "autor": data["autor"],
            "isbn": data["isbn"],
            "año_publicacion": data["año_publicacion"],
            "categoria": data["categoria"],
            "disponible": True
        }
        libros.append(nuevo_libro)
        return book_schema.jsonify(nuevo_libro), 201
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/books/<int:book_id>", methods=["PUT"])
@login_required
def update_book(book_id):
    libro = next((l for l in libros if l["id"] == book_id), None)
    if not libro:
        return {"error": "Libro no encontrado"}, 404
    
    data = request.json
    libro["titulo"] = data.get("titulo", libro["titulo"])
    libro["autor"] = data.get("autor", libro["autor"])
    libro["isbn"] = data.get("isbn", libro["isbn"])
    libro["año_publicacion"] = data.get("año_publicacion", libro["año_publicacion"])
    libro["categoria"] = data.get("categoria", libro["categoria"])
    
    return book_schema.jsonify(libro), 200

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
@login_required
def delete_book(book_id):
    global libros
    libro = next((l for l in libros if l["id"] == book_id), None)
    if not libro:
        return {"error": "Libro no encontrado"}, 404
    
    libros = [l for l in libros if l["id"] != book_id]
    return {"mensaje": "Libro eliminado exitosamente"}, 200

@app.route("/api/members", methods=["GET"])
@login_required
def get_members():
    return members_schema.jsonify(miembros), 200

@app.route("/api/members/<int:member_id>", methods=["GET"])
@login_required
def get_member(member_id):
    miembro = next((m for m in miembros if m["id"] == member_id), None)
    if miembro:
        return member_schema.jsonify(miembro), 200
    return {"error": "Miembro no encontrado"}, 404

@app.route("/api/members", methods=["POST"])
@login_required
def create_member():
    try:
        data = request.json
        errors = member_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        
        nuevo_miembro = {
            "id": max([m['id'] for m in miembros], default=0) + 1,
            "nombre": data["nombre"],
            "apellido": data["apellido"],
            "correo": data["correo"],
            "telefono": data["telefono"],
            "fecha_registro": datetime.now()
        }
        miembros.append(nuevo_miembro)
        return member_schema.jsonify(nuevo_miembro), 201
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/members/<int:member_id>", methods=["PUT"])
@login_required
def update_member(member_id):
    miembro = next((m for m in miembros if m["id"] == member_id), None)
    if not miembro:
        return {"error": "Miembro no encontrado"}, 404
    
    data = request.json
    miembro["nombre"] = data.get("nombre", miembro["nombre"])
    miembro["apellido"] = data.get("apellido", miembro["apellido"])
    miembro["correo"] = data.get("correo", miembro["correo"])
    miembro["telefono"] = data.get("telefono", miembro["telefono"])
    
    return member_schema.jsonify(miembro), 200

@app.route("/api/members/<int:member_id>", methods=["DELETE"])
@login_required
def delete_member(member_id):
    global miembros
    miembro = next((m for m in miembros if m["id"] == member_id), None)
    if not miembro:
        return {"error": "Miembro no encontrado"}, 404
    
    miembros = [m for m in miembros if m["id"] != member_id]
    return {"mensaje": "Miembro eliminado exitosamente"}, 200

@app.route("/api/loans", methods=["GET"])
@login_required
def get_loans():
    return loans_schema.jsonify(prestamos), 200

@app.route("/api/loans/<int:loan_id>", methods=["GET"])
@login_required
def get_loan(loan_id):
    prestamo = next((p for p in prestamos if p["id"] == loan_id), None)
    if prestamo:
        return loan_schema.jsonify(prestamo), 200
    return {"error": "Préstamo no encontrado"}, 404

@app.route("/api/loans", methods=["POST"])
@login_required
def create_loan():
    try:
        data = request.json
        errors = loan_schema.validate(data)
        if errors:
            return jsonify(errors), 400
        
        libro = next((l for l in libros if l["id"] == data["libro_id"]), None)
        if not libro:
            return {"error": "Libro no encontrado"}, 404
        
        miembro = next((m for m in miembros if m["id"] == data["miembro_id"]), None)
        if not miembro:
            return {"error": "Miembro no encontrado"}, 404
        
        if not libro["disponible"]:
            return {"error": "El libro no está disponible"}, 400
        
        nuevo_prestamo = {
            "id": max([p['id'] for p in prestamos], default=0) + 1,
            "libro_id": data["libro_id"],
            "miembro_id": data["miembro_id"],
            "fecha_prestamo": datetime.now(),
            "fecha_devolucion": None,
            "estado": "Activo"
        }
        prestamos.append(nuevo_prestamo)
        libro["disponible"] = False
        
        return loan_schema.jsonify(nuevo_prestamo), 201
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/loans/<int:loan_id>", methods=["PUT"])
@login_required
def update_loan(loan_id):
    prestamo = next((p for p in prestamos if p["id"] == loan_id), None)
    if not prestamo:
        return {"error": "Préstamo no encontrado"}, 404
    
    prestamo["fecha_devolucion"] = datetime.now()
    prestamo["estado"] = "Devuelto"
    
    libro = next((l for l in libros if l["id"] == prestamo["libro_id"]), None)
    if libro:
        libro["disponible"] = True
    
    return loan_schema.jsonify(prestamo), 200

@app.route("/api/loans/<int:loan_id>", methods=["DELETE"])
@login_required
def delete_loan(loan_id):
    global prestamos
    prestamo = next((p for p in prestamos if p["id"] == loan_id), None)
    if not prestamo:
        return {"error": "Préstamo no encontrado"}, 404
    
    prestamos = [p for p in prestamos if p["id"] != loan_id]
    return {"mensaje": "Préstamo eliminado exitosamente"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)