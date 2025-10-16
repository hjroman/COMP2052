from flask import Flask, request, jsonify

app = Flask(__name__)

usuarios = [
        {'id': 1, 
         "name" : "Joel", 
         "correo" : "joel@example.com"},

        {'id': 2, 
         "name" : "Brittannie", 
         "email" : "brittannie@example.com"}
    ]

@app.route("/info", methods=["GET"])
def informacion():
    data = {
        "Systema" : "Windows 11",
        "Computer" : "MSI GF63 Thin",
        "Python" : "3.13.7",
        "Flask" : "3.1.2"
    }
    return(jsonify(data))


@app.route("/crear_usuario", methods=["POST"])
def crear_suario():

    data = request.json
    if not data or not "name" in data or not "email" in data:
        return jsonify({"error": "Datos incompletos"}), 400
    
    nombre = data.get("name")
    return jsonify({"mensaje": f"Usuario {nombre} creado exitosamente!"})


@app.route("/usuarios", methods=["GET"])
def lista_usuarios():

    return(jsonify({"usuarios": usuarios}))




# Propuesta Estructura de datos:
#Lista de usuarios
users = [
    {"id": 1, "nombre": "Joel", "correo": "joel@example.com"},
    {"id": 2, "nombre": "Ana", "correo": "ana@example.com"}
]

#Lista de productos
products = [
    {"id": 1, "name": "Laptop", "price": 1200.00, "stock": 5},
    {"id": 2, "name": "Teclado", "price": 45.50, "stock": 20}
]

if __name__ == "__main__":
    app.run(debug=True)