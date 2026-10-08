import json
import mimetypes
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse

from presentation import routes


HOST = "localhost"
PORT = 8000

PRESENTATION_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = PRESENTATION_DIR / "templates"
STATIC_DIR = PRESENTATION_DIR / "static"

TEMPLATE_ROUTES = {
    "/": "index.html",
    "/menu.html": "menu.html",
    "/clientes.html": "clientes.html",
    "/pedidos.html": "pedidos.html",
}


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

    def enviar_archivo(self, ruta_archivo):
        if not ruta_archivo.exists() or not ruta_archivo.is_file():
            self.enviar_json(
                404,
                {
                    "error": "Archivo no encontrado.",
                },
            )
            return

        contenido = ruta_archivo.read_bytes()
        tipo = mimetypes.guess_type(
            str(ruta_archivo)
        )[0]

        if tipo is None:
            tipo = "application/octet-stream"

        self.send_response(200)
        self.send_header(
            "Content-Type",
            tipo,
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

    def servir_template(self, ruta):
        nombre_archivo = TEMPLATE_ROUTES[ruta]
        archivo = TEMPLATES_DIR / nombre_archivo
        self.enviar_archivo(archivo)

    def servir_archivo_statico(self, ruta):
        nombre_archivo = ruta.removeprefix(
            "/static/"
        )
        archivo = STATIC_DIR / nombre_archivo

        try:
            archivo.resolve().relative_to(
                STATIC_DIR.resolve()
            )
        except ValueError:
            self.enviar_json(
                403,
                {
                    "error": "Ruta no permitida.",
                },
            )
            return

        self.enviar_archivo(archivo)

    def leer_json(self):
        longitud = int(
            self.headers.get(
                "Content-Length",
                0,
            )
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

        if ruta.startswith("/api/"):
            if ruta == "/api/health":
                self.enviar_json(
                    200,
                    {
                        "estado": "ok",
                    },
                )
                return

            try:
                estado, respuesta = (
                    routes.obtener_recursos(ruta)
                )
                self.enviar_json(
                    estado,
                    respuesta,
                )

            except Exception as error:
                self.manejar_error(error)

            return

        if ruta.startswith("/static/"):
            self.servir_archivo_statico(ruta)
            return

        if ruta in TEMPLATE_ROUTES:
            self.servir_template(ruta)
            return

        self.enviar_json(
            404,
            {
                "error": "Recurso no encontrado.",
            },
        )

    def do_POST(self):
        ruta = urlparse(self.path).path

        try:
            datos = self.leer_json()

            estado, respuesta = (
                routes.crear_recurso(
                    ruta,
                    datos,
                )
            )

            self.enviar_json(
                estado,
                respuesta,
            )

        except Exception as error:
            self.manejar_error(error)

    def do_PATCH(self):
        ruta = urlparse(self.path).path

        try:
            datos = self.leer_json()

            estado, respuesta = (
                routes.actualizar_recurso(
                    ruta,
                    datos,
                )
            )

            self.enviar_json(
                estado,
                respuesta,
            )

        except Exception as error:
            self.manejar_error(error)

    def log_message(self, formato, *argumentos):
        print(
            f"[HTTP] {self.address_string()} "
            f"- {formato % argumentos}"
        )


class ServidorCafeOverflow(HTTPServer):
    allow_reuse_address = True


def iniciar_servidor():
    servidor = ServidorCafeOverflow(
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