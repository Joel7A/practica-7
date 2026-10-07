import bcrypt
from repositorio import AlmacenRepositorio


class AlmacenServicio:
    def __init__(self):
        self.repositorio = AlmacenRepositorio()

    def registrar_usuario(self, datos):

        nombre = datos.get("nombre")
        correo = datos.get("correo")
        password = datos.get("password")

        if not nombre or not correo or not password:
            return {"error": "Faltan datos requeridos"}, 400

        salt = bcrypt.gensalt()

        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

        resultado = self.repositorio.registrar_usuario(nombre, correo, password_hash)

        if resultado:
            return {"mensaje": "Usuario registrado exitosamente"}, 201

        return {"error": "Error al registrar el usuario"}, 500

    def login_usuario(self, correo, password):

        if not correo or not password:
            return {"error": "Faltan datos requeridos"}, 400

        usuario = self.repositorio.buscar_usuario_por_correo(correo)

        if not usuario:
            return {"error": "Usuario no encontrado"}, 404

        password_valida = bcrypt.checkpw(
            password.encode("utf-8"), usuario["password_hash"].encode("utf-8")
        )

        if password_valida:
            return {"mensaje": "Inicio de sesión exitoso"}, 200

        return {"error": "Contraseña incorrecta"}, 401

    def registrar_producto(self, datos):

        codigo_sku = datos.get("codigo_sku")
        nombre_producto = datos.get("nombre_producto")
        descripcion = datos.get("descripcion")
        stock = datos.get("stock")
        precio_unitario = datos.get("precio_unitario")
        categoria = datos.get("categoria")

        if (
            not codigo_sku
            or not nombre_producto
            or stock is None
            or precio_unitario is None
            or not categoria
        ):
            return {"error": "Faltan datos requeridos"}, 400

        if stock < 0:
            return {"error": "El stock no puede ser negativo"}, 400

        if precio_unitario <= 0:
            return {"error": "El precio unitario debe ser mayor a cero"}, 400

        resultado = self.repositorio.registrar_producto(
            codigo_sku, nombre_producto, descripcion, stock, precio_unitario, categoria
        )

        if resultado:
            return {"mensaje": "Producto registrado exitosamente"}, 201

        return {"error": "Error al registrar el producto"}, 500

    def listar_productos(self):

        productos = self.repositorio.listar_productos()

        if productos is None:
            return {"error": "Error al obtener los productos"}, 500

        return productos, 200
