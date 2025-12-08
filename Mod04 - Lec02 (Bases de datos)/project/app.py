from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# Configuración de la conexión a la base de datos
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'students_db'
}

# Función para obtener la conexión a la base de datos
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None

# Ruta principal
@app.route('/')
def index():
    return jsonify({
        "message": "API de Gestión de Estudiantes",
        "endpoints": {
            "GET /students": "Consultar todos los estudiantes",
            "GET /students/<id>": "Consultar un estudiante por ID",
            "POST /students": "Agregar un nuevo estudiante",
            "PUT /students/<id>": "Actualizar el grado de un estudiante",
            "DELETE /students/<id>": "Eliminar un estudiante"
        }
    })

# CREATE - Agregar un estudiante
@app.route('/students', methods=['POST'])
def create_student():
    try:
        data = request.json
        
        # Validar datos
        if not data or 'name' not in data or 'grade' not in data:
            return jsonify({"error": "Faltan datos requeridos (name, grade)"}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Error de conexión a la base de datos"}), 500
        
        cursor = connection.cursor()
        sql = "INSERT INTO students (name, grade) VALUES (%s, %s)"
        values = (data['name'], data['grade'])
        cursor.execute(sql, values)
        connection.commit()
        
        student_id = cursor.lastrowid
        cursor.close()
        connection.close()
        
        return jsonify({
            "message": "Estudiante creado exitosamente",
            "id": student_id,
            "name": data['name'],
            "grade": data['grade']
        }), 201
        
    except Error as e:
        return jsonify({"error": f"Error al crear estudiante: {str(e)}"}), 500

# READ - Consultar todos los estudiantes
@app.route('/students', methods=['GET'])
def get_students():
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Error de conexión a la base de datos"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students ORDER BY id")
        students = cursor.fetchall()
        cursor.close()
        connection.close()
        
        return jsonify({
            "count": len(students),
            "students": students
        }), 200
        
    except Error as e:
        return jsonify({"error": f"Error al consultar estudiantes: {str(e)}"}), 500

# READ - Consultar un estudiante por ID
@app.route('/students/<int:id>', methods=['GET'])
def get_student(id):
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Error de conexión a la base de datos"}), 500
        
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        student = cursor.fetchone()
        cursor.close()
        connection.close()
        
        if student:
            return jsonify(student), 200
        else:
            return jsonify({"error": "Estudiante no encontrado"}), 404
            
    except Error as e:
        return jsonify({"error": f"Error al consultar estudiante: {str(e)}"}), 500

# UPDATE - Actualizar el grado de un estudiante
@app.route('/students/<int:id>', methods=['PUT'])
def update_student(id):
    try:
        data = request.json
        
        # Validar datos
        if not data or 'grade' not in data:
            return jsonify({"error": "Falta el campo 'grade'"}), 400
        
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Error de conexión a la base de datos"}), 500
        
        cursor = connection.cursor()
        
        # Verificar si el estudiante existe
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({"error": "Estudiante no encontrado"}), 404
        
        # Actualizar el grado (y opcionalmente el nombre si se proporciona)
        if 'name' in data:
            sql = "UPDATE students SET name = %s, grade = %s WHERE id = %s"
            values = (data['name'], data['grade'], id)
        else:
            sql = "UPDATE students SET grade = %s WHERE id = %s"
            values = (data['grade'], id)
        
        cursor.execute(sql, values)
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "message": "Estudiante actualizado exitosamente",
            "id": id,
            "grade": data['grade']
        }), 200
        
    except Error as e:
        return jsonify({"error": f"Error al actualizar estudiante: {str(e)}"}), 500

# DELETE - Eliminar un estudiante
@app.route('/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    try:
        connection = get_db_connection()
        if connection is None:
            return jsonify({"error": "Error de conexión a la base de datos"}), 500
        
        cursor = connection.cursor()
        
        # Verificar si el estudiante existe
        cursor.execute("SELECT * FROM students WHERE id = %s", (id,))
        if not cursor.fetchone():
            cursor.close()
            connection.close()
            return jsonify({"error": "Estudiante no encontrado"}), 404
        
        # Eliminar el estudiante
        sql = "DELETE FROM students WHERE id = %s"
        cursor.execute(sql, (id,))
        connection.commit()
        cursor.close()
        connection.close()
        
        return jsonify({
            "message": "Estudiante eliminado exitosamente",
            "id": id
        }), 200
        
    except Error as e:
        return jsonify({"error": f"Error al eliminar estudiante: {str(e)}"}), 500

# Manejo de errores 404
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint no encontrado"}), 404

# Manejo de errores 500
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Error interno del servidor"}), 500

if __name__ == "__main__":
    print("Iniciando servidor Flask...")
    print("API disponible en: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)