from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

# Importar la capa de datos
from database import DatabaseLayer

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
        if session.get('user_rol') != 'admin':
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
        
        # Obtener usuario de la base de datos
        usuario = DatabaseLayer.get_user_by_username(username)
        
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
    # Obtener datos desde la base de datos
    libros = DatabaseLayer.get_all_books()
    miembros = DatabaseLayer.get_all_members()
    prestamos = DatabaseLayer.get_all_loans()
    
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
    libros = DatabaseLayer.get_all_books()
    return render_template('books.html', libros=libros)

@app.route('/members')
@login_required
def members_page():
    miembros = DatabaseLayer.get_all_members()
    return render_template('members.html', miembros=miembros)

@app.route('/loans')
@login_required
def loans_page():
    prestamos = DatabaseLayer.get_all_loans()
    libros = DatabaseLayer.get_all_books()
    miembros = DatabaseLayer.get_all_members()
    return render_template('loans.html', prestamos=prestamos, libros=libros, miembros=miembros)

@app.route('/users')
@admin_required
def users_page():
    usuarios = DatabaseLayer.get_all_users()
    return render_template('users.html', usuarios=usuarios)

# ==================== RUTAS DE FORMULARIOS - LIBROS ====================

@app.route('/books/create', methods=['POST'])
@login_required
def create_book_form():
    try:
        titulo = request.form.get('titulo')
        autor = request.form.get('autor')
        isbn = request.form.get('isbn')
        año_publicacion = int(request.form.get('año_publicacion'))
        categoria = request.form.get('categoria')
        
        book_id = DatabaseLayer.create_book(titulo, autor, isbn, año_publicacion, categoria)
        
        if book_id:
            flash(f'Libro "{titulo}" agregado exitosamente', 'success')
        else:
            flash('Error al crear libro', 'danger')
    except Exception as e:
        flash(f'Error al crear libro: {str(e)}', 'danger')
    return redirect(url_for('books_page'))

@app.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book_form(book_id):
    libro = DatabaseLayer.get_book_by_id(book_id)
    if libro:
        if DatabaseLayer.delete_book(book_id):
            flash(f'Libro "{libro["titulo"]}" eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar libro', 'danger')
    else:
        flash('Libro no encontrado', 'danger')
    return redirect(url_for('books_page'))

# ==================== RUTAS DE FORMULARIOS - MIEMBROS ====================

@app.route('/members/create', methods=['POST'])
@login_required
def create_member_form():
    try:
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        
        member_id = DatabaseLayer.create_member(nombre, apellido, correo, telefono)
        
        if member_id:
            flash(f'Miembro "{nombre} {apellido}" registrado exitosamente', 'success')
        else:
            flash('Error al registrar miembro', 'danger')
    except Exception as e:
        flash(f'Error al registrar miembro: {str(e)}', 'danger')
    return redirect(url_for('members_page'))

@app.route('/members/delete/<int:member_id>', methods=['POST'])
@login_required
def delete_member_form(member_id):
    miembro = DatabaseLayer.get_member_by_id(member_id)
    if miembro:
        if DatabaseLayer.delete_member(member_id):
            flash(f'Miembro "{miembro["nombre"]} {miembro["apellido"]}" eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar miembro', 'danger')
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
        
        libro = DatabaseLayer.get_book_by_id(libro_id)
        miembro = DatabaseLayer.get_member_by_id(miembro_id)
        
        if not libro:
            flash('Libro no encontrado', 'danger')
            return redirect(url_for('loans_page'))
        
        if not miembro:
            flash('Miembro no encontrado', 'danger')
            return redirect(url_for('loans_page'))
        
        if not libro['disponible']:
            flash('El libro no está disponible', 'warning')
            return redirect(url_for('loans_page'))
        
        loan_id = DatabaseLayer.create_loan(libro_id, miembro_id)
        
        if loan_id:
            flash(f'Préstamo registrado: "{libro["titulo"]}" para {miembro["nombre"]} {miembro["apellido"]}', 'success')
        else:
            flash('Error al crear préstamo', 'danger')
    except Exception as e:
        flash(f'Error al crear préstamo: {str(e)}', 'danger')
    return redirect(url_for('loans_page'))

@app.route('/loans/return/<int:loan_id>', methods=['POST'])
@login_required
def return_loan_form(loan_id):
    if DatabaseLayer.return_loan(loan_id):
        flash('Libro devuelto exitosamente', 'success')
    else:
        flash('Error al devolver libro', 'danger')
    return redirect(url_for('loans_page'))

@app.route('/loans/delete/<int:loan_id>', methods=['POST'])
@login_required
def delete_loan_form(loan_id):
    if DatabaseLayer.delete_loan(loan_id):
        flash('Préstamo eliminado exitosamente', 'success')
    else:
        flash('Error al eliminar préstamo', 'danger')
    return redirect(url_for('loans_page'))

# ==================== RUTAS DE FORMULARIOS - USUARIOS ====================

@app.route('/users/create', methods=['POST'])
@admin_required
def create_user_form():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        nombre = request.form.get('nombre')
        rol = request.form.get('rol')
        
        password_hash = generate_password_hash(password)
        
        if DatabaseLayer.create_user(username, password_hash, nombre, rol):
            flash(f'Usuario "{username}" creado exitosamente', 'success')
        else:
            flash('Error al crear usuario', 'danger')
    except Exception as e:
        flash(f'Error al crear usuario: {str(e)}', 'danger')
    return redirect(url_for('users_page'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user_form(user_id):
    if user_id == session['user_id']:
        flash('No puedes eliminar tu propio usuario', 'danger')
    else:
        if DatabaseLayer.delete_user(user_id):
            flash('Usuario eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar usuario', 'danger')
    return redirect(url_for('users_page'))

# ==================== REST API ENDPOINTS (JSON) ====================

@app.route("/api/books", methods=["GET"])
@login_required
def get_books():
    libros = DatabaseLayer.get_all_books()
    return books_schema.jsonify(libros), 200

@app.route("/api/books/<int:book_id>", methods=["GET"])
@login_required
def get_book(book_id):
    libro = DatabaseLayer.get_book_by_id(book_id)
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
        
        book_id = DatabaseLayer.create_book(
            data["titulo"], 
            data["autor"], 
            data["isbn"], 
            data["año_publicacion"], 
            data["categoria"]
        )
        
        if book_id:
            nuevo_libro = DatabaseLayer.get_book_by_id(book_id)
            return book_schema.jsonify(nuevo_libro), 201
        return {"error": "Error al crear libro"}, 400
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/books/<int:book_id>", methods=["PUT"])
@login_required
def update_book(book_id):
    libro = DatabaseLayer.get_book_by_id(book_id)
    if not libro:
        return {"error": "Libro no encontrado"}, 404
    
    data = request.json
    DatabaseLayer.update_book(
        book_id,
        data.get("titulo", libro["titulo"]),
        data.get("autor", libro["autor"]),
        data.get("isbn", libro["isbn"]),
        data.get("año_publicacion", libro["año_publicacion"]),
        data.get("categoria", libro["categoria"])
    )
    
    libro_actualizado = DatabaseLayer.get_book_by_id(book_id)
    return book_schema.jsonify(libro_actualizado), 200

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
@login_required
def delete_book(book_id):
    libro = DatabaseLayer.get_book_by_id(book_id)
    if not libro:
        return {"error": "Libro no encontrado"}, 404
    
    DatabaseLayer.delete_book(book_id)
    return {"mensaje": "Libro eliminado exitosamente"}, 200

@app.route("/api/members", methods=["GET"])
@login_required
def get_members():
    miembros = DatabaseLayer.get_all_members()
    return members_schema.jsonify(miembros), 200

@app.route("/api/members/<int:member_id>", methods=["GET"])
@login_required
def get_member(member_id):
    miembro = DatabaseLayer.get_member_by_id(member_id)
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
        
        member_id = DatabaseLayer.create_member(
            data["nombre"],
            data["apellido"],
            data["correo"],
            data["telefono"]
        )
        
        if member_id:
            nuevo_miembro = DatabaseLayer.get_member_by_id(member_id)
            return member_schema.jsonify(nuevo_miembro), 201
        return {"error": "Error al crear miembro"}, 400
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/members/<int:member_id>", methods=["PUT"])
@login_required
def update_member(member_id):
    miembro = DatabaseLayer.get_member_by_id(member_id)
    if not miembro:
        return {"error": "Miembro no encontrado"}, 404
    
    data = request.json
    DatabaseLayer.update_member(
        member_id,
        data.get("nombre", miembro["nombre"]),
        data.get("apellido", miembro["apellido"]),
        data.get("correo", miembro["correo"]),
        data.get("telefono", miembro["telefono"])
    )
    
    miembro_actualizado = DatabaseLayer.get_member_by_id(member_id)
    return member_schema.jsonify(miembro_actualizado), 200

@app.route("/api/members/<int:member_id>", methods=["DELETE"])
@login_required
def delete_member(member_id):
    miembro = DatabaseLayer.get_member_by_id(member_id)
    if not miembro:
        return {"error": "Miembro no encontrado"}, 404
    
    DatabaseLayer.delete_member(member_id)
    return {"mensaje": "Miembro eliminado exitosamente"}, 200

@app.route("/api/loans", methods=["GET"])
@login_required
def get_loans():
    prestamos = DatabaseLayer.get_all_loans()
    return loans_schema.jsonify(prestamos), 200

@app.route("/api/loans/<int:loan_id>", methods=["GET"])
@login_required
def get_loan(loan_id):
    prestamo = DatabaseLayer.get_loan_by_id(loan_id)
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
        
        libro = DatabaseLayer.get_book_by_id(data["libro_id"])
        if not libro:
            return {"error": "Libro no encontrado"}, 404
        
        miembro = DatabaseLayer.get_member_by_id(data["miembro_id"])
        if not miembro:
            return {"error": "Miembro no encontrado"}, 404
        
        if not libro["disponible"]:
            return {"error": "El libro no está disponible"}, 400
        
        loan_id = DatabaseLayer.create_loan(data["libro_id"], data["miembro_id"])
        
        if loan_id:
            nuevo_prestamo = DatabaseLayer.get_loan_by_id(loan_id)
            return loan_schema.jsonify(nuevo_prestamo), 201
        return {"error": "Error al crear préstamo"}, 400
    except Exception as e:
        return {"error": str(e)}, 400

@app.route("/api/loans/<int:loan_id>", methods=["PUT"])
@login_required
def update_loan(loan_id):
    prestamo = DatabaseLayer.get_loan_by_id(loan_id)
    if not prestamo:
        return {"error": "Préstamo no encontrado"}, 404
    
    DatabaseLayer.return_loan(loan_id)
    
    prestamo_actualizado = DatabaseLayer.get_loan_by_id(loan_id)
    return loan_schema.jsonify(prestamo_actualizado), 200

@app.route("/api/loans/<int:loan_id>", methods=["DELETE"])
@login_required
def delete_loan(loan_id):
    prestamo = DatabaseLayer.get_loan_by_id(loan_id)
    if not prestamo:
        return {"error": "Préstamo no encontrado"}, 404
    
    DatabaseLayer.delete_loan(loan_id)
    return {"mensaje": "Préstamo eliminado exitosamente"}, 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)