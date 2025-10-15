from flask import Flask, request

app = Flask(__name__)

@app.route("/info")
def informacion():
    return "Lección-02: App con Python 3.13.7 - Flask 3.1.2"

@app.route("/mensaje", methods=["POST"])
def saludo():
    data = request.json
    mensaje = data.get("saludo")
    return {"mensaje": f"{mensaje} bienvenido a mi app creada con Python y Flask!!"}, 200

if __name__ == "__main__":
    app.run(debug=True, port="5001")