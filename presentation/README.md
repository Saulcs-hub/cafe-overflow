# Frontend de Café Overflow

Esta carpeta es la **capa de presentación**. Aquí están las páginas que ve el cliente y también el servidor HTTP y las rutas que las entregan.

El frontend está hecho con HTML, CSS y JavaScript, sin frameworks ni librerías.

## Archivos

```text
presentation/
├── server.py                servidor HTTP (backend)
├── routes.py                rutas de la API (backend)
├── templates/
│   ├── index.html           inicio
│   ├── menu.html            menú y carrito
│   ├── clientes.html        registro y lista de clientes
│   └── pedidos.html         lista de pedidos
└── static/
    ├── css/styles.css       estilos de todas las páginas
    ├── js/app.js            lógica de las páginas
    └── img/                 fotos de los productos
```

## Páginas

| Página | Dirección | Qué permite |
|---|---|---|
| Inicio | `/` | Portada con accesos al menú y a los pedidos |
| Menú | `/menu.html` | Ver los productos, buscarlos, armar el carrito y confirmar el pedido |
| Pedidos | `/pedidos.html` | Ver los pedidos, filtrarlos por estado y avanzar su estado |
| Clientes | `/clientes.html` | Registrar un cliente y consultar su nivel, DevPoints y compras |

Todas comparten la misma barra lateral y el mismo archivo de estilos. En pantallas pequeñas la barra pasa a la parte de arriba.

## Cómo se comunica con el backend

Todo pasa por `app.js`, que usa `fetch` para llamar a la API y pinta en la página lo que el servidor responde.

| Acción en la página | Ruta que llama |
|---|---|
| Cargar el menú | `GET /api/productos` |
| Cargar la lista de clientes | `GET /api/clientes` |
| Registrar un cliente | `POST /api/clientes` |
| Ver el resumen del carrito | `POST /api/pedidos/cotizar` |
| Confirmar el pedido | `POST /api/pedidos` |
| Cargar los pedidos | `GET /api/pedidos` |
| Botón Avanzar | `PATCH /api/pedidos/{id}/estado` |

Si el servidor responde con un error, el mensaje que llega en `{"error": "..."}` se muestra tal cual en la página.

## Lo que el frontend no hace

Para respetar la separación de capas del taller:

- **No calcula nada.** El carrito solo guarda productos y cantidades. El subtotal, los descuentos y el total que se ven en el resumen llegan calculados desde el backend.
- **No valida reglas de negocio.** No revisa stock, pedidos pendientes ni DevPoints. Envía el pedido y muestra la respuesta.
- **No decide el siguiente estado** de un pedido. El botón Avanzar solo pide el cambio.
- **No consulta la base de datos.** Solo conoce las rutas `/api`.

Lo que sí valida es la forma de los datos: campos obligatorios, formato del correo y que las cantidades sean números.

Los buscadores y los filtros por estado solo muestran u ocultan lo que el servidor ya envió.

## Cómo verlo

El frontend lo entrega el servidor del proyecto. Desde la carpeta raíz:

```
python -m presentation.server
```

y luego se abre `http://localhost:8000` en el navegador. Los pasos completos están en el [README principal](../README.md).

Las páginas no funcionan abriendo los `.html` con doble clic, porque usan rutas como `/static/css/styles.css` y `/api/productos`, que solo existen cuando el servidor está corriendo.

## Notas

- Las fotos se cargan por el id del producto: `producto-1.jpg`, `producto-2.jpg`, etc. Si un producto no tiene foto se muestra la primera.
- Los nombres y precios del menú no están escritos en el HTML. Siempre salen de la base de datos.
- Los colores están definidos como variables al inicio de `styles.css`, por si se quiere cambiar la paleta.
