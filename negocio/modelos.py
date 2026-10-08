from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Producto:
    id: int | None
    nombre: str
    precio: int
    stock: int


@dataclass
class Cliente:
    id: int | None
    nombre: str
    correo: str
    nivel: str = "Junior"
    devpoints: int = 0
    compras_acumuladas: int = 0


@dataclass
class ItemPedido:
    producto_id: int
    cantidad: int
    precio_unitario: int


@dataclass
class Pedido:
    id: int | None
    cliente_id: int
    items: list[ItemPedido] = field(default_factory=list)
    estado: str = "Pendiente de pago"
    subtotal: int = 0
    descuento_nivel: int = 0
    descuento_devpoints: int = 0
    total: int = 0
    fecha: datetime = field(default_factory=datetime.now)