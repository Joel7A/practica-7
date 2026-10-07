from flask import Flask, jsonify, request
from servicio import AlmacenServicio


app = Flask(__name__)

servicio = AlmacenServicio()


@app.route("/api/auth/registro", methods=["POST"])
def registrar_usuario():

    datos_json = request.get_json()

    if not datos_json:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    respuesta, codigo_http = servicio.registrar_usuario(datos_json)

    return jsonify(respuesta), codigo_http


@app.route("/api/auth/login", methods=["POST"])
def login_usuario():

    try:
        datos_json = request.get_json()

        if not datos_json:
            return jsonify({"error": "No se proporcionaron datos"}), 400

        correo = datos_json.get("correo")
        password = datos_json.get("password")

        if not correo or not password:
            return jsonify({"error": "Faltan datos requeridos"}), 400

        respuesta, codigo_http = servicio.login_usuario(correo, password)

        return jsonify(respuesta), codigo_http

    except Exception as e:
        return jsonify({"error": f"Error al procesar la solicitud: {str(e)}"}), 500


@app.route("/api/almacen/productos", methods=["POST"])
def registrar_producto():

    datos_json = request.get_json()

    if not datos_json:
        return jsonify({"error": "No se proporcionaron datos"}), 400

    respuesta, codigo_http = servicio.registrar_producto(datos_json)

    return jsonify(respuesta), codigo_http


@app.route("/api/almacen/productos", methods=["GET"])
def listar_productos():

    respuesta, codigo_http = servicio.listar_productos()

    return jsonify(respuesta), codigo_http


if __name__ == "__main__":
    app.run(debug=True, port=5000)
