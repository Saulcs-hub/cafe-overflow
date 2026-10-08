# ☕ Café Overflow

Aplicación web para la gestión de pedidos del café temático para desarrolladores **Café Overflow – Dev & Coffee Lounge**.

El sistema permite consultar el menú, registrar clientes, crear pedidos, controlar el inventario, administrar niveles de lealtad y redimir DevPoints.

## 👥 Equipo

- **Carlos Saúl Villabona** — Backend, lógica de negocio y persistencia.
- **Alejandro Jiménez** — Frontend, interfaz web y experiencia de usuario.

## 🎯 Objetivo

Desarrollar una aplicación web utilizando una arquitectura **N-Tier de tres capas**, aplicando separación de responsabilidades y aislamiento entre:

1. Capa de presentación.
2. Capa de negocio.
3. Capa de persistencia.

El proyecto se desarrolla sin frameworks, utilizando directamente las tecnologías requeridas.

## 🛠️ Tecnologías

- HTML5
- CSS3
- JavaScript
- Python estándar
- SQLite
- Git y GitHub
- Arquitectura C4

## 🏗️ Arquitectura

```text
Interfaz web
HTML + CSS + JavaScript
        │
        ▼
Capa de presentación
Servidor HTTP y rutas
        │
        ▼
Capa de negocio
Servicios y reglas del sistema
        │
        ▼
Capa de persistencia
DAO y conexión SQLite
        │
        ▼
Base de datos SQLite
```

### Capa de presentación

Se encarga de:

- Mostrar las vistas.
- Capturar información de formularios.
- Validar entradas básicas.
- Enviar solicitudes HTTP.
- Mostrar respuestas y mensajes al usuario.

No calcula totales ni aplica reglas de negocio.

### Capa de negocio

Se encarga de:

- Calcular los totales de los pedidos.
- Aplicar descuentos por nivel.
- Validar el stock.
- Validar pedidos pendientes.
- Gestionar los estados de los pedidos.
- Administrar DevPoints.
- Procesar los ascensos de nivel.

### Capa de persistencia

Se encarga de:

- Conectarse con SQLite.
- Guardar información.
- Consultar productos, clientes y pedidos.
- Actualizar el stock.
- Actualizar los datos de los clientes.

Los DAO no contienen reglas de negocio.

## ☕ Funcionalidades

### Productos

- Registrar productos.
- Consultar el menú.
- Consultar precios.
- Consultar stock disponible.
- Actualizar el inventario.

### Clientes

- Registrar clientes.
- Consultar información del cliente.
- Asignar nivel de lealtad.
- Acumular compras.
- Acumular y redimir DevPoints.

### Pedidos

- Crear pedidos.
- Agregar productos y cantidades.
- Calcular el total.
- Aplicar descuentos.
- Consultar pedidos.
- Cambiar el estado del pedido.

## ⭐ Reglas de lealtad

| Nivel | Descuento |
|---|---:|
| Junior | 5 % |
| Mid | 10 % |
| Senior | 15 % |

### Ascensos automáticos

- Todo cliente nuevo inicia como **Junior**.
- Al alcanzar o superar **$500.000** en compras completadas, asciende a **Mid**.
- Al alcanzar o superar **$1.500.000** en compras completadas, asciende a **Senior**.

### DevPoints

- Por cada **$20.000 consumidos**, el cliente recibe 1 DevPoint.
- Cada DevPoint equivale a **$200 de descuento**.
- Los DevPoints pueden redimirse en una compra posterior.
- El descuento total nunca puede ser menor que cero.

## 📦 Estados de los pedidos

```text
Pendiente de pago
        ↓
En preparación
        ↓
Listo
        ↓
Entregado
```

Las compras acumuladas y los DevPoints se actualizan cuando el pedido se completa.

## 🚫 Validaciones principales

- No se puede pedir una cantidad superior al stock disponible.
- No se puede crear otro pedido si el cliente tiene uno pendiente de pago.
- No se pueden redimir más DevPoints de los disponibles.
- Un pedido no puede quedar con un total negativo.
- Un cliente nuevo siempre comienza en el nivel Junior.

## 📁 Estructura del proyecto

```text
cafe-overflow/
├── presentation/
├── negocio/
├── persistencia/
├── tests/
├── diagramas/
├── README.md
└── .gitignore
```

## 📐 Diagramas C4

### Nivel 1: Contexto

Muestra la relación entre el cliente y el sistema Café Overflow.

![C4 Nivel 1 - Contexto](docs/diagramas/c4-nivel-1-contexto.jpeg)

### Nivel 2: Contenedores

Muestra la interfaz web, la aplicación Python y la base de datos SQLite.

![C4 Nivel 2 - Contenedores](docs/diagramas/c4-nivel-2-contenedores.jpeg)

### Nivel 3: Componentes

Muestra los componentes internos de las capas de presentación, negocio y persistencia.

![C4 Nivel 3 - Componentes](docs/diagramas/c4-nivel-3-componentes.jpeg)

## 🌿 Ramas de GitHub

```text
main       → versión estable
develop    → integración del proyecto
frontend   → desarrollo de la interfaz
backend    → desarrollo del servidor y la lógica
```

## 🚀 Ejecución del proyecto

Próximamente se documentarán los pasos para:

1. Clonar el repositorio.
2. Inicializar la base de datos.
3. Ejecutar el servidor Python.
4. Abrir la aplicación en el navegador.

## 📚 Contexto académico

Proyecto desarrollado para el taller de **Arquitectura de Software – Modelo N-Tier**, aplicando:

- Separación de responsabilidades.
- Aislamiento de capas.
- Arquitectura de tres niveles.
- Patrón DAO.
- Diagramas C4.
- Desarrollo colaborativo con GitHub.
