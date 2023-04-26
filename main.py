from flask import Flask, g
import psycopg2

app = Flask (__name__)

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


