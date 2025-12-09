from flask import Flask, request, jsonify
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from shared.database import DatabaseLayer

app = Flask(__name__)

@app.route('/books', methods=['GET'])
def get_books():
    books = DatabaseLayer.get_all_books()
    return jsonify(books), 200

@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = DatabaseLayer.get_book_by_id(book_id)
    if book:
        return jsonify(book), 200
    return jsonify({"error": "Libro no encontrado"}), 404

@app.route('/books', methods=['POST'])
def create_book():
    data = request.json
    book_id = DatabaseLayer.create_book(
        data['titulo'],
        data['autor'],
        data['isbn'],
        data['año_publicacion'],
        data['categoria']
    )
    
    if book_id:
        return jsonify({"message": "Libro creado", "id": book_id}), 201
    return jsonify({"error": "Error al crear libro"}), 400

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.json
    success = DatabaseLayer.update_book(
        book_id,
        data['titulo'],
        data['autor'],
        data['isbn'],
        data['año_publicacion'],
        data['categoria']
    )
    
    if success:
        return jsonify({"message": "Libro actualizado"}), 200
    return jsonify({"error": "Error al actualizar libro"}), 400

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    success = DatabaseLayer.delete_book(book_id)
    if success:
        return jsonify({"message": "Libro eliminado"}), 200
    return jsonify({"error": "Libro no encontrado"}), 404

@app.route('/books/<int:book_id>/availability', methods=['PUT'])
def update_availability(book_id):
    data = request.json
    success = DatabaseLayer.update_book_availability(book_id, data['disponible'])
    if success:
        return jsonify({"message": "Disponibilidad actualizada"}), 200
    return jsonify({"error": "Error al actualizar"}), 400

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"service": "books", "status": "healthy"}), 200

if __name__ == "__main__":
    print("📚 Servicio de Libros iniciado en puerto 5002")
    app.run(port=5002, debug=True, use_reloader=False)
