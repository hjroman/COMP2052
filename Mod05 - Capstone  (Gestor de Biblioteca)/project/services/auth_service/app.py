from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.database import DatabaseLayer

app = Flask(__name__)

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    user = DatabaseLayer.get_user_by_username(username)
    
    if user and check_password_hash(user['password'], password):
        return jsonify({
            "success": True,
            "user": {
                "id": user['id'],
                "username": user['username'],
                "nombre": user['nombre'],
                "rol": user['rol']
            }
        }), 200
    else:
        return jsonify({"success": False, "message": "Credenciales incorrectas"}), 401

@app.route('/auth/users', methods=['GET'])
def get_users():
    users = DatabaseLayer.get_all_users()
    return jsonify(users), 200

@app.route('/auth/users', methods=['POST'])
def create_user():
    data = request.json
    password_hash = generate_password_hash(data['password'])
    
    success = DatabaseLayer.create_user(
        data['username'],
        password_hash,
        data['nombre'],
        data['rol']
    )
    
    if success:
        return jsonify({"message": "Usuario creado exitosamente"}), 201
    return jsonify({"error": "Error al crear usuario"}), 400

@app.route('/auth/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = DatabaseLayer.delete_user(user_id)
    if success:
        return jsonify({"message": "Usuario eliminado"}), 200
    return jsonify({"error": "Usuario no encontrado"}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"service": "auth", "status": "healthy"}), 200

if __name__ == "__main__":
    print("🔐 Servicio de Autenticación iniciado en puerto 5001")
    app.run(port=5001, debug=True, use_reloader=False)
