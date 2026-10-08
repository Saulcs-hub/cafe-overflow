import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse

from presentation import routes


HOST = "localhost"
PORT = 8000


class ServidorHTTP(BaseHTTPRequestHandler):
    """
    Servidor HTTP básico para Café Overflow.
    """

    def enviar_json(self, estado, datos):
        contenido = json.dumps(
            datos,
            ensure_ascii=False,
        ).encode("utf-8")

        self.send_response(estado)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8",
        )
        self.send_header(
            "Content-Length",
            str(len(contenido)),
        )
        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )
        self.end_headers()
        self.wfile.write(contenido)

    def leer_json(self):
        longitud = int(
            self.headers.get("Content-Length", 0)
        )

        contenido = self.rfile.read(longitud)

        if not contenido:
            return {}

        return json.loads(
            contenido.decode("utf-8")
        )

    def manejar_error(self, error):
        if isinstance(error, ValueError):
            self.enviar_json(
                400,
                {
                    "error": str(error),
                },
            )
            return

        self.enviar_json(
            500,
            {
                "error": "Error interno del servidor.",
            },
        )

        print(f"Error interno: {error}")

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header(
            "Access-Control-Allow-Origin",
            "*",
        )
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, PATCH, OPTIONS",
        )
        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type",
        )
        self.end_headers()

    def do_GET(self):
        ruta = urlparse(self.path).path

        if ruta == "/":
            self.enviar_json(
                200,
                {
                    "mensaje": "API de Café Overflow funcionando."
                },
            )
            return

        if ruta == "/api/health":
            self.enviar_json(
                200,
                {
                    "estado": "ok",
                },
            )
            return

        try:
            estado, respuesta = routes.obtener_recursos(
                ruta
            )
            self.enviar_json(estado, respuesta)

        except Exception as error:
            self.manejar_error(error)

    def do_POST(self):
        ruta = urlparse(self.path).path

        try:
            datos = self.leer_json()
            estado, respuesta = routes.crear_recurso(
                ruta,
                datos,
            )
            self.enviar_json(estado, respuesta)

        except Exception as error:
            self.manejar_error(error)

    def do_PATCH(self):
        ruta = urlparse(self.path).path

        try:
            datos = self.leer_json()
            estado, respuesta = routes.actualizar_recurso(
                ruta,
                datos,
            )
            self.enviar_json(estado, respuesta)

        except Exception as error:
            self.manejar_error(error)

    def log_message(self, formato, *argumentos):
        print(
            f"[HTTP] {self.address_string()} "
            f"- {formato % argumentos}"
        )


class ServidorCaféOverflow(HTTPServer):
    allow_reuse_address = True


def iniciar_servidor():
    servidor = ServidorCaféOverflow(
        (HOST, PORT),
        ServidorHTTP,
    )

    print(
        f"Servidor iniciado en "
        f"http://{HOST}:{PORT}"
    )

    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor detenido.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    iniciar_servidor()