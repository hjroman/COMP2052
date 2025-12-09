from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.database import DatabaseLayer

app = Flask(__name__)

@app.route('/members', methods=['GET'])
def get_members():
    members = DatabaseLayer.get_all_members()
    return jsonify(members), 200

@app.route('/members/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = DatabaseLayer.get_member_by_id(member_id)
    if member:
        return jsonify(member), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

@app.route('/members', methods=['POST'])
def create_member():
    data = request.json
    member_id = DatabaseLayer.create_member(
        data['nombre'],
        data['apellido'],
        data['correo'],
        data['telefono']
    )
    
    if member_id:
        return jsonify({"message": "Miembro creado", "id": member_id}), 201
    return jsonify({"error": "Error al crear miembro"}), 400

@app.route('/members/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    data = request.json
    success = DatabaseLayer.update_member(
        member_id,
        data['nombre'],
        data['apellido'],
        data['correo'],
        data['telefono']
    )
    
    if success:
        return jsonify({"message": "Miembro actualizado"}), 200
    return jsonify({"error": "Error al actualizar miembro"}), 400

@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = DatabaseLayer.delete_member(member_id)
    if success:
        return jsonify({"message": "Miembro eliminado"}), 200
    return jsonify({"error": "Miembro no encontrado"}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"service": "members", "status": "healthy"}), 200

if __name__ == "__main__":
    print("👥 Servicio de Miembros iniciado en puerto 5003")
    app.run(port=5003, debug=True, use_reloader=False)
