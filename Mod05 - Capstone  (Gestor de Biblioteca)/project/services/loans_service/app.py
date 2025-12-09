from flask import Flask, request, jsonify
import requests
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.database import DatabaseLayer
from shared.config import ServiceConfig

app = Flask(__name__)

@app.route('/loans', methods=['GET'])
def get_loans():
    loans = DatabaseLayer.get_all_loans()
    return jsonify(loans), 200

@app.route('/loans/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    loan = DatabaseLayer.get_loan_by_id(loan_id)
    if loan:
        return jsonify(loan), 200
    return jsonify({"error": "Préstamo no encontrado"}), 404

@app.route('/loans', methods=['POST'])
def create_loan():
    data = request.json
    libro_id = data['libro_id']
    miembro_id = data['miembro_id']
    
    try:
        book_response = requests.get(f"{ServiceConfig.BOOKS_SERVICE_URL}/books/{libro_id}")
        if book_response.status_code != 200:
            return jsonify({"error": "Libro no encontrado"}), 404
        
        book = book_response.json()
        if not book['disponible']:
            return jsonify({"error": "Libro no disponible"}), 400
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicarse con servicio de libros: {str(e)}"}), 500
    
    try:
        member_response = requests.get(f"{ServiceConfig.MEMBERS_SERVICE_URL}/members/{miembro_id}")
        if member_response.status_code != 200:
            return jsonify({"error": "Miembro no encontrado"}), 404
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error al comunicarse con servicio de miembros: {str(e)}"}), 500
    
    loan_id = DatabaseLayer.create_loan(libro_id, miembro_id)
    
    if not loan_id:
        return jsonify({"error": "Error al crear préstamo"}), 400
    
    try:
        requests.put(
            f"{ServiceConfig.BOOKS_SERVICE_URL}/books/{libro_id}/availability",
            json={"disponible": False}
        )
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar disponibilidad: {e}")
    
    return jsonify({"message": "Préstamo creado exitosamente", "id": loan_id}), 201

@app.route('/loans/<int:loan_id>/return', methods=['PUT'])
def return_loan(loan_id):
    loan = DatabaseLayer.get_loan_by_id(loan_id)
    if not loan:
        return jsonify({"error": "Préstamo no encontrado"}), 404
    
    success = DatabaseLayer.return_loan(loan_id)
    if not success:
        return jsonify({"error": "Error al devolver préstamo"}), 400
    
    try:
        requests.put(
            f"{ServiceConfig.BOOKS_SERVICE_URL}/books/{loan['libro_id']}/availability",
            json={"disponible": True}
        )
    except requests.exceptions.RequestException as e:
        print(f"Error al actualizar disponibilidad: {e}")
    
    return jsonify({"message": "Préstamo devuelto exitosamente"}), 200

@app.route('/loans/<int:loan_id>', methods=['DELETE'])
def delete_loan(loan_id):
    success = DatabaseLayer.delete_loan(loan_id)
    if success:
        return jsonify({"message": "Préstamo eliminado"}), 200
    return jsonify({"error": "Préstamo no encontrado"}), 404

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"service": "loans", "status": "healthy"}), 200

if __name__ == "__main__":
    print("📖 Servicio de Préstamos iniciado en puerto 5004")
    app.run(port=5004, debug=True, use_reloader=False)
