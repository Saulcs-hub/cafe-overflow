import sqlite3
from pathlib import Path


PERSISTENCIA_DIR = Path(__file__).resolve().parent
BASE_DIR = PERSISTENCIA_DIR.parent

DATABASE_PATH = PERSISTENCIA_DIR / "cafe_overflow.db"
SCHEMA_PATH = PERSISTENCIA_DIR / "esquema.sql"


def obtener_conexion():
    """
    Crea y devuelve una conexión a la base de datos SQLite.
    """
    conexion = sqlite3.connect(DATABASE_PATH)
    conexion.row_factory = sqlite3.Row
    conexion.execute("PRAGMA foreign_keys = ON")
    return conexion


def inicializar_base_datos():
    """
    Crea las tablas definidas en esquema.sql si todavía no existen.
    """
    esquema = SCHEMA_PATH.read_text(encoding="utf-8")

    with obtener_conexion() as conexion:
        conexion.executescript(esquema)


if __name__ == "__main__":
    inicializar_base_datos()
    print(f"Base de datos creada en: {DATABASE_PATH}")