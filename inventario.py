# gestion_ferreteria.py
# -----------------------------------------------------------------------------
# Sistema Avanzado de Gestión de Inventarios para una Ferretería
# Autor: Gemini (Google AI)
# Descripción: Este script combina la Programación Orientada a Objetos,
# el uso de colecciones (diccionarios) y una base de datos SQLite para
# crear un sistema de inventario robusto y eficiente.
# -----------------------------------------------------------------------------

import sqlite3

# =============================================================================
# SECCIÓN 1: CLASE MODELO - Producto
# Define la estructura de los datos con los que trabajaremos.
# =============================================================================

class Producto:
    """
    Representa un producto en el inventario de la ferretería.

    Atributos:
        id (int): Identificador único del producto.
        nombre (str): Nombre del producto.
        cantidad (int): Cantidad disponible en stock.
        precio (float): Precio unitario del producto.
    """
    def __init__(self, nombre, cantidad, precio, id_producto=None):
        """Inicializa un objeto Producto."""
        self.id = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def __str__(self):
        """Devuelve una representación en cadena del producto para ser impresa."""
        return (f"ID: {self.id:<5} | "
                f"Nombre: {self.nombre:<30} | "
                f"Cantidad: {self.cantidad:<10} | "
                f"Precio: ${self.precio:>8.2f}")

# =============================================================================
# SECCIÓN 2: CLASE CONTROLADORA - Inventario
# Contiene toda la lógica de negocio y la interacción con la base de datos.
# =============================================================================

class Inventario:
    """
    Gestiona las operaciones del inventario, incluyendo la interacción
    con la base de datos SQLite y el manejo de una colección en memoria.
    """
    def __init__(self, db_path='ferreteria.db'):
        """
        Inicializa el inventario, conecta a la BD y carga los productos.
        """
        self.db_path = db_path
        self._crear_tabla()
        # El DICCIONARIO es la colección elegida para optimizar el acceso
        # a los productos por su ID, lo que lo hace extremadamente rápido.
        self.productos = self._cargar_productos()
        print("✔ Inventario cargado y listo.")

    def _conectar(self):
        """Crea y devuelve una conexión a la base de datos."""
        try:
            conn = sqlite3.connect(self.db_path)
            return conn
        except sqlite3.Error as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            return None

    def _crear_tabla(self):
        """Crea la tabla 'productos' en la base de datos si no existe."""
        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS productos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        precio REAL NOT NULL
                    )
                """)
                conn.commit()
            except sqlite3.Error as e:
                print(f"❌ Error al crear la tabla: {e}")
            finally:
                conn.close()

    def _cargar_productos(self):
        """Carga todos los productos de la BD en el diccionario en memoria."""
        conn = self._conectar()
        productos_dict = {}
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM productos ORDER BY nombre ASC")
                filas = cursor.fetchall()
                for fila in filas:
                    id_prod, nombre, cantidad, precio = fila
                    producto = Producto(nombre, cantidad, precio, id_prod)
                    productos_dict[id_prod] = producto # Usando ID como clave
            except sqlite3.Error as e:
                print(f"❌ Error al cargar productos: {e}")
            finally:
                conn.close()
        return productos_dict

    def anadir_producto(self, nombre, cantidad, precio):
        """Añade un nuevo producto a la BD y al inventario en memoria."""
        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                               (nombre, cantidad, precio))
                conn.commit()
                id_nuevo = cursor.lastrowid
                producto_nuevo = Producto(nombre, cantidad, precio, id_nuevo)
                self.productos[id_nuevo] = producto_nuevo
                print(f"✔ Producto '{nombre}' añadido con éxito.")
            except sqlite3.Error as e:
                print(f"❌ Error al añadir el producto: {e}")
            finally:
                conn.close()

    def eliminar_producto(self, id_producto):
        """Elimina un producto de la BD y del inventario por su ID."""
        if id_producto not in self.productos:
            print(f"❌ Error: No existe un producto con el ID {id_producto}.")
            return

        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM productos WHERE id = ?", (id_producto,))
                conn.commit()
                del self.productos[id_producto] # Sincroniza el diccionario
                print(f"✔ Producto con ID {id_producto} eliminado con éxito.")
            except sqlite3.Error as e:
                print(f"❌ Error al eliminar el producto: {e}")
            finally:
                conn.close()

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        """Actualiza la cantidad y/o el precio de un producto existente."""
        if id_producto not in self.productos:
            print(f"❌ Error: No existe un producto con el ID {id_producto}.")
            return

        producto_actual = self.productos[id_producto]
        nueva_cantidad = cantidad if cantidad is not None else producto_actual.cantidad
        nuevo_precio = precio if precio is not None else producto_actual.precio

        conn = self._conectar()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE productos SET cantidad = ?, precio = ? WHERE id = ?",
                               (nueva_cantidad, nuevo_precio, id_producto))
                conn.commit()
                producto_actual.cantidad = nueva_cantidad # Sincroniza el objeto
                producto_actual.precio = nuevo_precio
                print(f"✔ Producto con ID {id_producto} actualizado con éxito.")
            except sqlite3.Error as e:
                print(f"❌ Error al actualizar el producto: {e}")
            finally:
                conn.close()

    def buscar_producto_por_nombre(self, nombre):
        """Busca productos en memoria cuyo nombre contenga el texto buscado."""
        resultados = [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]
        
        if not resultados:
            print(f"No se encontraron productos que coincidan con '{nombre}'.")
            return

        print("\n--- Resultados de la Búsqueda ---")
        for producto in resultados:
            print(producto)
        print("---------------------------------")

    def mostrar_inventario(self):
        """Muestra todos los productos del inventario de forma ordenada."""
        print("\n--- Inventario Completo de la Ferretería ---")
        if not self.productos:
            print("El inventario está vacío.")
        else:
            # Ordenamos los productos por nombre para una mejor visualización
            productos_ordenados = sorted(self.productos.values(), key=lambda p: p.nombre)
            for producto in productos_ordenados:
                print(producto)
        print("------------------------------------------")

# =============================================================================
# SECCIÓN 3: INTERFAZ DE USUARIO (VISTA)
# Punto de entrada de la aplicación y menú interactivo.
# =============================================================================

def mostrar_menu():
    """Muestra el menú de opciones al usuario."""
    print("\n--- Sistema de Gestión de Inventario de Ferretería ---")
    print("1. Añadir nuevo producto")
    print("2. Eliminar producto por ID")
    print("3. Actualizar producto por ID")
