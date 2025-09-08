import os
import json
import csv
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# --- Configuración de la App y la Base de Datos ---

# Obtiene la ruta absoluta del directorio donde se encuentra este archivo.
# Es una forma robusta de asegurarse de que las rutas a los archivos funcionen
# sin importar desde dónde se ejecute la aplicación.
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Configura la URI de la base de datos para usar SQLite.
# El archivo 'usuarios.db' se creará en la carpeta 'database' del proyecto.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database/usuarios.db')

# Desactiva una característica de SQLAlchemy que no necesitamos y que consume recursos.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa la extensión SQLAlchemy, conectándola con nuestra app Flask.
db = SQLAlchemy(app)


# --- Definición del Modelo (Tabla de la Base de Datos) ---

class Usuario(db.Model):
    """
    Define la estructura de la tabla 'usuario' en la base de datos.
    Cada atributo de la clase corresponde a una columna en la tabla.
    """
    id = db.Column(db.Integer, primary_key=True)  # Clave primaria, autoincremental por defecto.
    nombre = db.Column(db.String(80), nullable=False)  # Campo de texto, no puede ser nulo.
    mensaje = db.Column(db.String(200), nullable=False) # Campo de texto, no puede ser nulo.

    def __repr__(self):
        # Representación en cadena del objeto, útil para depuración.
        return f'<Usuario {self.nombre}>'

# --- Creación de la Base de Datos y Tablas ---

# Este bloque se asegura de que las tablas de la base de datos se creen
# a partir de los modelos definidos. Solo se ejecuta una vez cuando la app arranca.
with app.app_context():
    db.create_all()


# --- Rutas de la Aplicación ---

@app.route('/')
def index():
    """Ruta principal que muestra el formulario."""
    return render_template('formulario.html')

# --- 1. Persistencia con Archivos TXT ---

@app.route('/guardar_txt', methods=['POST'])
def guardar_txt():
    """Recibe datos del formulario y los guarda en un archivo de texto."""
    nombre = request.form['nombre']
    mensaje = request.form['mensaje']
    
    # Abre 'datos.txt' en modo 'append' (añadir al final) y escribe una nueva línea.
    with open('datos/datos.txt', 'a', encoding='utf-8') as archivo:
        archivo.write(f"Nombre: {nombre}, Mensaje: {mensaje}\n")
        
    return redirect(url_for('ver_datos_txt'))

@app.route('/datos_txt')
def ver_datos_txt():
    """Lee y muestra el contenido del archivo de texto."""
    try:
        with open('datos/datos.txt', 'r', encoding='utf-8') as archivo:
            contenido = archivo.readlines()
        return render_template('resultado.html', titulo="Datos Guardados (TXT)", datos=contenido)
    except FileNotFoundError:
        return "El archivo de texto aún no existe. Envía datos desde el formulario primero."

# --- 2. Persistencia con Archivos JSON ---

def leer_json():
    """Función auxiliar para leer el contenido del archivo JSON."""
    try:
        with open('datos/datos.json', 'r', encoding='utf-8') as archivo:
            return json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        # Si el archivo no existe o está vacío, devuelve una lista vacía.
        return []

def escribir_json(datos):
    """Función auxiliar para escribir datos en el archivo JSON."""
    with open('datos/datos.json', 'w', encoding='utf-8') as archivo:
        # 'indent=4' formatea el JSON para que sea legible.
        json.dump(datos, archivo, indent=4, ensure_ascii=False)

@app.route('/guardar_json', methods=['POST'])
def guardar_json():
    """Recibe datos y los añade al archivo JSON."""
    datos_existentes = leer_json()
    nuevo_dato = {"nombre": request.form['nombre'], "mensaje": request.form['mensaje']}
    datos_existentes.append(nuevo_dato)
    escribir_json(datos_existentes)
    
    return redirect(url_for('ver_datos_json'))

@app.route('/datos_json')
def ver_datos_json():
    """Lee y muestra el contenido del archivo JSON."""
    datos = leer_json()
    # Convertimos los dicts a strings para una visualización simple en la plantilla
    datos_str = [json.dumps(item, ensure_ascii=False) for item in datos]
    return render_template('resultado.html', titulo="Datos Guardados (JSON)", datos=datos_str)

# --- 3. Persistencia con Archivos CSV ---

@app.route('/guardar_csv', methods=['POST'])
def guardar_csv():
    """Recibe datos y los añade como una nueva fila en un archivo CSV."""
    nombre = request.form['nombre']
    mensaje = request.
