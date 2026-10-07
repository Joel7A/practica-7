import os

import mysql.connector

from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


class AlmacenRepositorio:
    def __init__(self):
        self.host = os.getenv("DB_HOST")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

    def obtener_conexion(self):
        try:
            conexion = mysql.connector.Connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )
            return conexion

        except Error as e:
            print(f"Error al conectar a la base de datos {e}")
            return None

    def registrar_usuario(self, nombre, correo, password_hash):
        conexion = self.obtener_conexion()

        if conexion is None:
            return False

        try:
            cursor = conexion.cursor()

            query = """
            INSERT INTO usuarios_almacen(
            nombre, correo, password_hash
            ) VALUES(%s,%s,%s)"""

            cursor.execute(query, (nombre, correo, password_hash))
            conexion.commit()
            return True
        except Error as e:
            print(f"Error al registrar usuario: {e}")
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def buscar_usuario_por_correo(self, correo):
        conexion = self.obtener_conexion()

        if conexion is None:
            return None

        try:
            cursor = conexion.cursor(dictionary=True)
            query = """
                SELECT * FROM usuarios_almacen WHERE correo = %s 
            """
            cursor.execute(query, (correo,))
            usuario = cursor.fetchone()

            return usuario
        except Error as a:
            print(f"Error al burcar usuario {a}")
            return None
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    # registrar y listar productos
    def registrar_producto(
        self,
        codigo_sku,
        nombre_producto,
        descripcion,
        stock,
        precio_unitario,
        categoria,
    ):
        conexion = self.obtener_conexion()
        if conexion is None:
            return False
        try:
            cursor = conexion.cursor(dictionary=True)

            query = """
                INSERT INTO productos_inventario(codigo_sku, nombre_producto, descripcion, stock, precio_unitario, categoria)
                VALUES(%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(
                query,
                (
                    codigo_sku,
                    nombre_producto,
                    descripcion,
                    stock,
                    precio_unitario,
                    categoria,
                ),
            )

            conexion.commit()
            return True

        except Error as e:
            print(f"Error al registrar productos: {e}")
            return False
        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()

    def listar_productos(self):
        conexion = self.obtener_conexion()

        if conexion is None:
            return None
        try:
            cursor = conexion.cursor()
            query = """
                    SELECT * FROM productos_inventario
                """
            cursor.execute(query)
            productos = cursor.fetchall()
            return productos

        except Error as e:
            print(f"Error al listar los productos: {e}")
            return None

        finally:
            if conexion.is_connected():
                cursor.close()
                conexion.close()
