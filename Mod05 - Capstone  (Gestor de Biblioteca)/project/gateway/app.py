from flask import Flask, render_template, request, redirect, url_for, flash, session
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from shared.config import ServiceConfig
from functools import wraps

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')
app.secret_key = 'tu_clave_secreta_super_segura_123'

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
        
        try:
            response = requests.post(
                f"{ServiceConfig.AUTH_SERVICE_URL}/auth/login",
                json={"username": username, "password": password}
            )
            
            if response.status_code == 200:
                data = response.json()
                user = data['user']
                session['user_id'] = user['id']
                session['user_nombre'] = user['nombre']
                session['user_rol'] = user['rol']
                flash('¡Bienvenido de nuevo!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash('Usuario o contraseña incorrectos', 'danger')
        except Exception as e:
            flash(f'Error al conectar con el servicio de autenticación: {str(e)}', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    try:
        books_response = requests.get(f"{ServiceConfig.BOOKS_SERVICE_URL}/books")
        members_response = requests.get(f"{ServiceConfig.MEMBERS_SERVICE_URL}/members")
        loans_response = requests.get(f"{ServiceConfig.LOANS_SERVICE_URL}/loans")
        
        libros = books_response.json() if books_response.status_code == 200 else []
        miembros = members_response.json() if members_response.status_code == 200 else []
        prestamos = loans_response.json() if loans_response.status_code == 200 else []
        
        stats = {
            'total_libros': len(libros),
            'libros_disponibles': sum(1 for l in libros if l['disponible']),
            'total_miembros': len(miembros),
            'prestamos_activos': sum(1 for p in prestamos if p['estado'] == 'Activo')
        }
        return render_template('dashboard.html', **stats)
    except Exception as e:
        flash(f'Error al obtener datos: {str(e)}', 'danger')
        return render_template('dashboard.html', total_libros=0, libros_disponibles=0, 
                             total_miembros=0, prestamos_activos=0)

@app.route('/books')
@login_required
def books_page():
    try:
        response = requests.get(f"{ServiceConfig.BOOKS_SERVICE_URL}/books")
        libros = response.json() if response.status_code == 200 else []
        return render_template('books.html', libros=libros)
    except Exception as e:
        flash(f'Error al obtener libros: {str(e)}', 'danger')
        return render_template('books.html', libros=[])

@app.route('/books/create', methods=['POST'])
@login_required
def create_book_form():
    try:
        data = {
            'titulo': request.form.get('titulo'),
            'autor': request.form.get('autor'),
            'isbn': request.form.get('isbn'),
            'año_publicacion': int(request.form.get('año_publicacion')),
            'categoria': request.form.get('categoria')
        }
        
        response = requests.post(f"{ServiceConfig.BOOKS_SERVICE_URL}/books", json=data)
        
        if response.status_code == 201:
            flash(f'Libro "{data["titulo"]}" agregado exitosamente', 'success')
        else:
            flash('Error al crear libro', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('books_page'))

@app.route('/books/delete/<int:book_id>', methods=['POST'])
@login_required
def delete_book_form(book_id):
    try:
        response = requests.delete(f"{ServiceConfig.BOOKS_SERVICE_URL}/books/{book_id}")
        if response.status_code == 200:
            flash('Libro eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar libro', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('books_page'))

@app.route('/members')
@login_required
def members_page():
    try:
        response = requests.get(f"{ServiceConfig.MEMBERS_SERVICE_URL}/members")
        miembros = response.json() if response.status_code == 200 else []
        return render_template('members.html', miembros=miembros)
    except Exception as e:
        flash(f'Error al obtener miembros: {str(e)}', 'danger')
        return render_template('members.html', miembros=[])

@app.route('/members/create', methods=['POST'])
@login_required
def create_member_form():
    try:
        data = {
            'nombre': request.form.get('nombre'),
            'apellido': request.form.get('apellido'),
            'correo': request.form.get('correo'),
            'telefono': request.form.get('telefono')
        }
        
        response = requests.post(f"{ServiceConfig.MEMBERS_SERVICE_URL}/members", json=data)
        
        if response.status_code == 201:
            flash(f'Miembro "{data["nombre"]} {data["apellido"]}" registrado exitosamente', 'success')
        else:
            flash('Error al registrar miembro', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('members_page'))

@app.route('/members/delete/<int:member_id>', methods=['POST'])
@login_required
def delete_member_form(member_id):
    try:
        response = requests.delete(f"{ServiceConfig.MEMBERS_SERVICE_URL}/members/{member_id}")
        if response.status_code == 200:
            flash('Miembro eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar miembro', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('members_page'))

@app.route('/loans')
@login_required
def loans_page():
    try:
        loans_response = requests.get(f"{ServiceConfig.LOANS_SERVICE_URL}/loans")
        books_response = requests.get(f"{ServiceConfig.BOOKS_SERVICE_URL}/books")
        members_response = requests.get(f"{ServiceConfig.MEMBERS_SERVICE_URL}/members")
        
        prestamos = loans_response.json() if loans_response.status_code == 200 else []
        libros = books_response.json() if books_response.status_code == 200 else []
        miembros = members_response.json() if members_response.status_code == 200 else []
        
        return render_template('loans.html', prestamos=prestamos, libros=libros, miembros=miembros)
    except Exception as e:
        flash(f'Error al obtener datos: {str(e)}', 'danger')
        return render_template('loans.html', prestamos=[], libros=[], miembros=[])

@app.route('/loans/create', methods=['POST'])
@login_required
def create_loan_form():
    try:
        data = {
            'libro_id': int(request.form.get('libro_id')),
            'miembro_id': int(request.form.get('miembro_id'))
        }
        
        response = requests.post(f"{ServiceConfig.LOANS_SERVICE_URL}/loans", json=data)
        
        if response.status_code == 201:
            flash('Préstamo registrado exitosamente', 'success')
        else:
            error_msg = response.json().get('error', 'Error desconocido')
            flash(f'Error: {error_msg}', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('loans_page'))

@app.route('/loans/return/<int:loan_id>', methods=['POST'])
@login_required
def return_loan_form(loan_id):
    try:
        response = requests.put(f"{ServiceConfig.LOANS_SERVICE_URL}/loans/{loan_id}/return")
        if response.status_code == 200:
            flash('Libro devuelto exitosamente', 'success')
        else:
            flash('Error al devolver libro', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('loans_page'))

@app.route('/loans/delete/<int:loan_id>', methods=['POST'])
@login_required
def delete_loan_form(loan_id):
    try:
        response = requests.delete(f"{ServiceConfig.LOANS_SERVICE_URL}/loans/{loan_id}")
        if response.status_code == 200:
            flash('Préstamo eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar préstamo', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('loans_page'))

@app.route('/users')
@admin_required
def users_page():
    try:
        response = requests.get(f"{ServiceConfig.AUTH_SERVICE_URL}/auth/users")
        usuarios = response.json() if response.status_code == 200 else []
        return render_template('users.html', usuarios=usuarios)
    except Exception as e:
        flash(f'Error al obtener usuarios: {str(e)}', 'danger')
        return render_template('users.html', usuarios=[])

@app.route('/users/create', methods=['POST'])
@admin_required
def create_user_form():
    try:
        data = {
            'username': request.form.get('username'),
            'password': request.form.get('password'),
            'nombre': request.form.get('nombre'),
            'rol': request.form.get('rol')
        }
        
        response = requests.post(f"{ServiceConfig.AUTH_SERVICE_URL}/auth/users", json=data)
        
        if response.status_code == 201:
            flash(f'Usuario "{data["username"]}" creado exitosamente', 'success')
        else:
            flash('Error al crear usuario', 'danger')
    except Exception as e:
        flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('users_page'))

@app.route('/users/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user_form(user_id):
    if user_id == session['user_id']:
        flash('No puedes eliminar tu propio usuario', 'danger')
    else:
        try:
            response = requests.delete(f"{ServiceConfig.AUTH_SERVICE_URL}/auth/users/{user_id}")
            if response.status_code == 200:
                flash('Usuario eliminado exitosamente', 'success')
            else:
                flash('Error al eliminar usuario', 'danger')
        except Exception as e:
            flash(f'Error: {str(e)}', 'danger')
    return redirect(url_for('users_page'))

if __name__ == "__main__":
    print("🌐 API Gateway iniciado en puerto 5000")
    print("=" * 60)
    print("Accede a: http://localhost:5000")
    print("=" * 60)
    app.run(port=5000, debug=True, use_reloader=False)
