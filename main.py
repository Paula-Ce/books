from flask import Flask, g, jsonify, request
import psycopg2

app = Flask (__name__) # Esto lo utiliza FLASK para saber dónde está ubicado nuestro archivo principal. Sería lo mismo que pasarle "__main__"

# Configuración de la conexión a la base de datos

def get_db():
    db = getattr (g, "_database", None)
    # Del módulo "g" obtenemos el atributo "database", y si no hay nada, nos devuelve "None".
    # La variable g es del entorno Flask y se utiliza para guardar los datos que vamos a utilizar en 1 consulta.
    # En este caso sería la base de datos.
    # g se crea al realizar la solicitud y se destruye luego.
    if db is None:
        db = psycopg2.connect(
                                user="postgres",
                                password="PIKqPhxx35Ymhm3MIgdR",
                                host="containers-us-west-17.railway.app",
                                port="5679",
                                database="railway"
                                )
    return db

@app.teardown_appcontext 
# Este decorador es para registrar una función. Se utiliza al final de cada solicitud y aqui se encarga de cerrar la conexión de la BBDD.
def close_connection (exception):
    db = getattr (g, "_database", None)
    if db is not None:
        db.close()

# Ruta para la página de inicio

@app.route("/", methods=["GET"])
# Al poner la barra se entiende que se trata de la "base"
def home():
    conn = get_db() # Creamos la conexión. Me conecto a la BBDD. Esta función la hemos definido arriba.
    cursor = conn.cursor () # Creamos un cursor, para apuntar al principio de la BBDD, Y luego se irá moviendo. Es una especie de "puntero".
    cursor.execute ("SELECT * FROM books_table") # Esto nos va a devolver todo lo que hay en esta tabla (por el *)
    # "Execute" es una sentencia de la clase "cursor" que ejecuta una query SQL en la base de datos.
    totalRows = cursor.fetchall() # Con esto obtenemos las columnas. Esto es un diccionario.

    num_libros = len(totalRows)

    cursor.close() # Hay que cerrar el cursor para si vuelvo a ejecutar la query no esté apuntando a dónde nos hemos quedado.

    home_display = f"""
    <h1>API libros</h1>
    <p>Esta es una API que contiene {num_libros} libros.</p>"""

    return home_display


# 1. Ruta para obtener todos los libros de la BBDD

@app.route("/books", methods = ["GET"])
def get_books():
    conn = get_db()
    cursor = conn.cursor ()
    cursor.execute ("SELECT * FROM books_table") 
    books = cursor.fetchall() 
    cursor.close()

    return jsonify(books)


# 2. Ruta para añdir 1 libro a la BBDD

@app.route("/resources/book/add", methods = ["POST"])
def add_book():
       
    # Obtener datos del cuerpo de la petición
    book = request.get_json()

    # Obtenemos los datos del libro a través de los parámetros de la petición
    # author = request.args.get ("author")

    # Almacenar los datos en variables
    author = book["author"]
    year = book["year"]
    title = book["title"]
    description = book["description"]
    id_book = book ["id"]

    # Crear la conexión a la base de datos
    conn = get_db()
    cursor = conn.cursor ()
    cursor.execute("INSERT INTO books_table (id, author, year, title, description) VALUES (%s, %s, %s, %s, %s)", (id_book, author, year, title, description))
    conn.commit()
    cursor.close()

    return jsonify ({"message" : "El libro ha sido añadido correctamente"})


# 3. Ruta para eliminar un libro por su ID

@app.route("/resources/book/delete/<int:id>", methods = ["DELETE"])
def delete_book(id):
    conn = get_db()
    cursor = conn.cursor()
    cursor .execute("DELETE FROM books_table WHERE id = %s", (id,)) # Se pone coma detrás de "id" para que entienda que es un SET y no unos paréntesis normales.
    conn.commit()
    cursor.close()

    return jsonify ({"message": "El libro ha sido eliminado correctamente."})


# 3. Ruta para actualizar un libro

@app.route("/resources/book/update", methods = ["PUT"])
def update_book():

    # Almacenar los datos en las variables. Esta vez en lugar de obtenerlo por el body vamos a obtenerlo por parámetros
    # Si los parámetros son cortos, se puede hacer así. 
    # Si son larguísimos, al meterlo por parámetros se pone todo en la ruta, por lo que es un churro. En ese caso mejor por el body.

    title = request.args["title"]
    year = request.args["year"]

    # Conectar con la base de datos
    conn = get_db()
    cursor = conn.cursor()
    cursor .execute("UPDATE books_table SET year = %s WHERE title = %s", (year, title)) # Ojo que mantengamos el dato "title" y cambiemos "year" y no al revés.
    conn.commit()
    cursor.close()

    return jsonify ({"message": "El libro ha sido actualizado correctamente."})


# Ejecutar la aplicación

# Es una buena práctica que el código que se ejecuta al ejecutar el archivo sea el siguiente: "if__name__ == "__main__"
# Esto es para que el servidor sólo se ejecute cuando se ejecute el archivo main.py, y no cuando se importe desde otro archivo.

# Si tu archivo Python es sólo un script simple que se ejecuta de manera directa, y no tiene la intención de ser reutilizado como un módulo
# en otro lugar, entonces no necesitas nacesariamente utilizarlo.

if __name__ == '__main__':
    app.run(debug = True)