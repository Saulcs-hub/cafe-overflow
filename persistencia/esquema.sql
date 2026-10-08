PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio INTEGER NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0)
);

CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    correo TEXT NOT NULL UNIQUE,
    nivel TEXT NOT NULL DEFAULT 'Junior'
        CHECK (nivel IN ('Junior', 'Mid', 'Senior')),
    devpoints INTEGER NOT NULL DEFAULT 0 CHECK (devpoints >= 0),
    compras_acumuladas INTEGER NOT NULL DEFAULT 0
        CHECK (compras_acumuladas >= 0)
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER NOT NULL,
    estado TEXT NOT NULL DEFAULT 'Pendiente de pago'
        CHECK (
            estado IN (
                'Pendiente de pago',
                'En preparación',
                'Listo',
                'Entregado'
            )
        ),
    subtotal INTEGER NOT NULL DEFAULT 0 CHECK (subtotal >= 0),
    descuento_nivel INTEGER NOT NULL DEFAULT 0 CHECK (descuento_nivel >= 0),
    descuento_devpoints INTEGER NOT NULL DEFAULT 0
        CHECK (descuento_devpoints >= 0),
    total INTEGER NOT NULL DEFAULT 0 CHECK (total >= 0),
    fecha TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);

CREATE TABLE IF NOT EXISTS pedido_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pedido_id INTEGER NOT NULL,
    producto_id INTEGER NOT NULL,
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario INTEGER NOT NULL CHECK (precio_unitario >= 0),
    FOREIGN KEY (pedido_id) REFERENCES pedidos(id),
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);