// Café Overflow - frontend
// Este archivo solo pide datos al backend y los muestra en pantalla.
// Los totales, descuentos, DevPoints y validaciones de negocio los hace el servidor.

const API = '/api';

// ---------- Funciones de apoyo ----------

async function pedir(ruta, opciones = {}) {
  const respuesta = await fetch(API + ruta, {
    headers: { 'Content-Type': 'application/json' },
    ...opciones,
  });

  let datos = null;
  try {
    datos = await respuesta.json();
  } catch (e) {
    datos = null;
  }

  if (!respuesta.ok) {
    const texto = datos && datos.error ? datos.error : 'No se pudo completar la solicitud.';
    throw new Error(texto);
  }
  return datos;
}

function mostrarMensaje(id, texto, tipo) {
  const caja = document.getElementById(id);
  caja.textContent = texto;
  caja.className = 'mensaje ' + tipo;
}

function ocultarMensaje(id) {
  const caja = document.getElementById(id);
  caja.textContent = '';
  caja.className = 'mensaje';
}

function pesos(valor) {
  return '$ ' + Number(valor).toLocaleString('es-CO');
}

function escapar(texto) {
  const div = document.createElement('div');
  div.textContent = texto;
  return div.innerHTML;
}

function contiene(texto, busqueda) {
  return String(texto).toLowerCase().includes(busqueda.toLowerCase());
}

function foto(id) {
  return '/static/img/producto-' + id + '.jpg';
}

// Si un producto no tiene foto se usa la primera
function fotoDeRespaldo(img) {
  img.addEventListener('error', function () {
    img.src = foto(1);
  }, { once: true });
}

// ---------- Página: menú ----------

let productos = [];
let clientes = [];
const carrito = {}; // producto_id -> cantidad
let turnoCotizacion = 0;

const ICONO_BASURA =
  '<svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
  '<path d="M4 7h16M10 11v6M14 11v6M6 7l1 13h10l1-13M9 7V4h6v3"/></svg>';

async function iniciarMenu() {
  try {
    productos = await pedir('/productos');
    pintarProductos();
  } catch (error) {
    mostrarMensaje('mensaje-productos', error.message, 'error');
  }

  try {
    clientes = await pedir('/clientes');
    pintarSelectClientes();
  } catch (error) {
    mostrarMensaje('mensaje-pedido', error.message, 'error');
  }

  document.getElementById('buscar-producto').addEventListener('input', pintarProductos);
  document.getElementById('devpoints').addEventListener('input', cotizar);
  document.getElementById('cliente').addEventListener('change', function () {
    pintarInfoCliente();
    cotizar();
  });
  document.getElementById('form-pedido').addEventListener('submit', enviarPedido);
}

function pintarProductos() {
  const busqueda = document.getElementById('buscar-producto').value.trim();
  const contenedor = document.getElementById('productos');
  contenedor.innerHTML = '';

  productos
    .filter(function (p) { return contiene(p.nombre, busqueda); })
    .forEach(function (p) {
      const tarjeta = document.createElement('article');
      tarjeta.className = 'producto';
      tarjeta.innerHTML =
        '<img src="' + foto(p.id) + '" alt="' + escapar(p.nombre) + '">' +
        '<div class="datos">' +
        '<h3>' + escapar(p.nombre) + '</h3>' +
        '<div class="stock">Disponibles: ' + p.stock + '</div>' +
        '<div class="abajo">' +
        '<span>' + pesos(p.precio) + '</span>' +
        '<button class="redondo" type="button" title="Agregar al carrito">+</button>' +
        '</div>' +
        '</div>';

      fotoDeRespaldo(tarjeta.querySelector('img'));
      tarjeta.querySelector('button').addEventListener('click', function () {
        cambiarCantidad(p.id, 1);
      });
      contenedor.appendChild(tarjeta);
    });
}

function cambiarCantidad(id, cambio) {
  const nueva = (carrito[id] || 0) + cambio;
  if (nueva > 0) {
    carrito[id] = nueva;
  } else {
    delete carrito[id];
  }
  pintarCarrito();
}

function quitarDelCarrito(id) {
  delete carrito[id];
  pintarCarrito();
}

function pintarCarrito() {
  const lista = document.getElementById('lista-carrito');
  lista.innerHTML = '';

  const elegidos = productos.filter(function (p) { return carrito[p.id]; });
  let unidades = 0;

  elegidos.forEach(function (p) {
    unidades += carrito[p.id];

    const li = document.createElement('li');
    li.className = 'item';
    li.innerHTML =
      '<img src="' + foto(p.id) + '" alt="">' +
      '<div class="nombre">' + escapar(p.nombre) +
      '<small>' + pesos(p.precio) + '</small>' +
      '<div class="controles">' +
      '<button type="button" title="Quitar uno">-</button>' +
      '<span>' + carrito[p.id] + '</span>' +
      '<button type="button" title="Agregar uno">+</button>' +
      '</div>' +
      '</div>' +
      '<button class="basura" type="button" title="Quitar del carrito">' + ICONO_BASURA + '</button>';

    fotoDeRespaldo(li.querySelector('img'));
    const botones = li.querySelectorAll('.controles button');
    botones[0].addEventListener('click', function () { cambiarCantidad(p.id, -1); });
    botones[1].addEventListener('click', function () { cambiarCantidad(p.id, 1); });
    li.querySelector('.basura').addEventListener('click', function () { quitarDelCarrito(p.id); });
    lista.appendChild(li);
  });

  if (elegidos.length === 0) {
    lista.innerHTML = '<li class="vacio">Aún no has agregado productos.</li>';
  }
  document.getElementById('contador').textContent = unidades;
  cotizar();
}

function pintarSelectClientes() {
  const select = document.getElementById('cliente');
  clientes.forEach(function (c) {
    const opcion = document.createElement('option');
    opcion.value = c.id;
    opcion.textContent = c.nombre;
    select.appendChild(opcion);
  });
}

function clienteElegido() {
  const id = Number(document.getElementById('cliente').value);
  return clientes.find(function (c) { return c.id === id; });
}

function pintarInfoCliente() {
  const cliente = clienteElegido();
  document.getElementById('info-cliente').textContent = cliente
    ? 'Nivel ' + cliente.nivel + ' - ' + cliente.devpoints + ' DevPoints disponibles'
    : '';
}

// Datos del pedido tal como los espera el backend
function armarPedido() {
  return {
    cliente_id: Number(document.getElementById('cliente').value),
    items: Object.keys(carrito).map(function (id) {
      return { producto_id: Number(id), cantidad: carrito[id] };
    }),
    devpoints_a_redimir: Number(document.getElementById('devpoints').value) || 0,
  };
}

// Pide al backend la cuenta del carrito. Aquí no se calcula nada.
async function cotizar() {
  const resumen = document.getElementById('resumen');
  const pedido = armarPedido();

  if (pedido.items.length === 0 || !pedido.cliente_id) {
    turnoCotizacion++;
    resumen.innerHTML = '<p class="vacio">Agrega productos y elige un cliente para ver el total.</p>';
    return;
  }

  // Si llegan varias respuestas, solo se usa la del último cambio
  const turno = ++turnoCotizacion;
  try {
    const r = await pedir('/pedidos/cotizar', { method: 'POST', body: JSON.stringify(pedido) });
    if (turno !== turnoCotizacion) return;
    ocultarMensaje('mensaje-pedido');
    pintarResumen(r);
  } catch (error) {
    if (turno !== turnoCotizacion) return;
    resumen.innerHTML = '';
    mostrarMensaje('mensaje-pedido', error.message, 'error');
  }
}

// Muestra los valores tal como los calculó el backend
function pintarResumen(r) {
  const cliente = clienteElegido();
  const puntos = Number(document.getElementById('devpoints').value) || 0;

  document.getElementById('resumen').innerHTML =
    '<ul class="resumen">' +
    '<li><span>Subtotal</span><span>' + pesos(r.subtotal) + '</span></li>' +
    '<li class="descuento"><span>Descuento por nivel (' + escapar(cliente.nivel) + ')</span><span>- ' + pesos(r.descuento_nivel) + '</span></li>' +
    '<li class="descuento"><span>DevPoints (' + puntos + ' puntos)</span><span>- ' + pesos(r.descuento_devpoints) + '</span></li>' +
    '<li class="total"><span>Total</span><span>' + pesos(r.total) + '</span></li>' +
    '</ul>';
}

async function enviarPedido(evento) {
  evento.preventDefault();
  ocultarMensaje('mensaje-pedido');

  const pedido = armarPedido();
  if (pedido.items.length === 0) {
    mostrarMensaje('mensaje-pedido', 'Agrega al menos un producto.', 'error');
    return;
  }

  try {
    const r = await pedir('/pedidos', { method: 'POST', body: JSON.stringify(pedido) });

    // Se vacía el carrito y se vuelven a pedir los datos actualizados
    Object.keys(carrito).forEach(function (id) { delete carrito[id]; });
    document.getElementById('devpoints').value = 0;
    pintarCarrito();
    mostrarMensaje('mensaje-pedido',
      'Pedido #' + r.pedido_id + ' registrado. Total: ' + pesos(r.total) + '. Estado: ' + r.estado + '.', 'ok');

    productos = await pedir('/productos');
    pintarProductos();
    clientes = await pedir('/clientes');
    pintarInfoCliente();
  } catch (error) {
    mostrarMensaje('mensaje-pedido', error.message, 'error');
  }
}

// ---------- Página: clientes ----------

let listaClientes = [];

async function iniciarClientes() {
  document.getElementById('form-cliente').addEventListener('submit', registrarCliente);
  document.getElementById('buscar-cliente').addEventListener('input', pintarClientes);
  await cargarClientes();
}

async function cargarClientes() {
  try {
    listaClientes = await pedir('/clientes');
    pintarClientes();
  } catch (error) {
    mostrarMensaje('mensaje-lista', error.message, 'error');
  }
}

function pintarClientes() {
  const busqueda = document.getElementById('buscar-cliente').value.trim();
  const tabla = document.getElementById('tabla-clientes');
  tabla.innerHTML = '';

  const visibles = listaClientes.filter(function (c) {
    return contiene(c.nombre, busqueda) || contiene(c.correo, busqueda);
  });

  if (visibles.length === 0) {
    tabla.innerHTML = '<tr><td colspan="5" class="vacio">No hay clientes para mostrar.</td></tr>';
    return;
  }

  visibles.forEach(function (c) {
    const fila = document.createElement('tr');
    fila.innerHTML =
      '<td>' + escapar(c.nombre) + '</td>' +
      '<td>' + escapar(c.correo) + '</td>' +
      '<td><span class="etiqueta">' + escapar(c.nivel) + '</span></td>' +
      '<td>' + c.devpoints + '</td>' +
      '<td>' + pesos(c.acumulado) + '</td>';
    tabla.appendChild(fila);
  });
}

async function registrarCliente(evento) {
  evento.preventDefault();
  ocultarMensaje('mensaje-cliente');

  const cliente = {
    nombre: document.getElementById('nombre').value.trim(),
    correo: document.getElementById('correo').value.trim(),
  };

  try {
    await pedir('/clientes', { method: 'POST', body: JSON.stringify(cliente) });
    mostrarMensaje('mensaje-cliente', 'Cliente registrado.', 'ok');
    evento.target.reset();
    await cargarClientes();
  } catch (error) {
    mostrarMensaje('mensaje-cliente', error.message, 'error');
  }
}

// ---------- Página: pedidos ----------

let listaPedidos = [];
let filtroEstado = '';

// Color de la etiqueta según el estado
const CLASE_ESTADO = {
  'Pendiente de pago': 'pendiente',
  'En preparación': 'preparacion',
  'Listo': 'listo',
  'Entregado': 'entregado',
};

async function iniciarPedidos() {
  document.getElementById('buscar-pedido').addEventListener('input', pintarPedidos);

  document.querySelectorAll('#filtros button').forEach(function (boton) {
    boton.addEventListener('click', function () {
      document.querySelector('#filtros .activo').classList.remove('activo');
      boton.classList.add('activo');
      filtroEstado = boton.dataset.estado;
      pintarPedidos();
    });
  });

  await cargarPedidos();
}

async function cargarPedidos() {
  try {
    listaPedidos = await pedir('/pedidos');
    pintarPedidos();
  } catch (error) {
    mostrarMensaje('mensaje-pedidos', error.message, 'error');
  }
}

function pintarPedidos() {
  const busqueda = document.getElementById('buscar-pedido').value.trim();
  const tabla = document.getElementById('tabla-pedidos');
  tabla.innerHTML = '';

  const visibles = listaPedidos.filter(function (p) {
    const porEstado = filtroEstado === '' || p.estado === filtroEstado;
    const porTexto = contiene(p.cliente_nombre, busqueda) ||
      p.items.some(function (i) { return contiene(i.nombre, busqueda); });
    return porEstado && porTexto;
  });

  if (visibles.length === 0) {
    tabla.innerHTML = '<tr><td colspan="7" class="vacio">No hay pedidos para mostrar.</td></tr>';
    return;
  }

  visibles.forEach(function (p) {
    const detalle = p.items.map(function (i) {
      return escapar(i.nombre) + ' x ' + i.cantidad;
    }).join('<br>');

    const fila = document.createElement('tr');
    fila.innerHTML =
      '<td>#' + p.id + '</td>' +
      '<td>' + escapar(p.cliente_nombre) + '</td>' +
      '<td>' + detalle + '</td>' +
      '<td>' + pesos(p.total) + '</td>' +
      '<td><span class="etiqueta ' + (CLASE_ESTADO[p.estado] || '') + '">' + escapar(p.estado) + '</span></td>' +
      '<td>' + escapar(p.fecha) + '</td>' +
      '<td></td>';

    if (p.estado !== 'Entregado') {
      const boton = document.createElement('button');
      boton.className = 'boton pequeno';
      boton.textContent = 'Avanzar';
      boton.addEventListener('click', function () { avanzarPedido(p.id); });
      fila.lastElementChild.appendChild(boton);
    }
    tabla.appendChild(fila);
  });
}

// El backend decide cuál es el siguiente estado
async function avanzarPedido(id) {
  ocultarMensaje('mensaje-pedidos');
  try {
    await pedir('/pedidos/' + id + '/estado', { method: 'PATCH' });
    await cargarPedidos();
  } catch (error) {
    mostrarMensaje('mensaje-pedidos', error.message, 'error');
  }
}

// ---------- Arranque ----------

document.addEventListener('DOMContentLoaded', function () {
  const pagina = document.body.dataset.pagina;
  if (pagina === 'menu') iniciarMenu();
  if (pagina === 'clientes') iniciarClientes();
  if (pagina === 'pedidos') iniciarPedidos();
});
