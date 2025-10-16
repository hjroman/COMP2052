from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {"title": "Gestor de Biblioteca", "message": "Gestor de Libros de Biblioteca"}
    return render_template('index.html', data=data)

@app.route('/libros')
def lista_libros():
    data = {
            "libros": ["Lord of the Rings: The Fellowship of the Ring", 
                       "Lord of the Rings: The Two Towers", 
                       "Lord of the Rings: The Return of the King", 
                       "Harry Potter and the Prisoner of Azkaban", 
                       "Harry Potter and the Goblet of Fire",
                       "The Chronicles of Narnia: The Lion, the Witch and the Wardrobe",
                       "The Chronicles of Narnia: Prince Caspian"]}
    return render_template("libros.html", **data)

@app.route('/autores')
def lista_autores():
    data = {
            "autores": ["John Ronald Reuel Tolkien", 
                        "J.K. Rowling",
                        "C.S Lewis",
                        "Kyoko Tsuchiya",
                        "Iori Tamaki"]                 
    }
    return render_template("autores.html", **data)

if __name__ == '__main__':
    app.run(debug=True)