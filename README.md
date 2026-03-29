# 📦 Sistema de Inventario

Sistema de gestión de inventario por consola desarrollado en Python. Permite realizar operaciones CRUD sobre productos, consultar estadísticas del negocio y persistir los datos en archivos JSON entre sesiones.

---

## 🗂️ Estructura del proyecto

```
inventario/
│
├── app.py          # Punto de entrada: menú principal y flujo de usuario
├── servicios.py    # Módulo CRUD + estadísticas
├── archivos.py     # Módulo de persistencia JSON (guardar / cargar)
└── README.md
```

---

## ⚙️ Requisitos

- Python **3.10** o superior
- No requiere librerías externas (solo módulos de la biblioteca estándar: `json`, `os`)

---

## 🚀 Cómo ejecutar

```bash
python app.py
```

Al iniciar, se muestra el menú principal y el programa se mantiene activo hasta que el usuario elige **Salir** (opción 9).

---

## 🧭 Menú principal

```
╔══════════════════════════════════╗
║     SISTEMA DE INVENTARIO        ║
╠══════════════════════════════════╣
║  1. Agregar producto             ║
║  2. Mostrar inventario           ║
║  3. Buscar producto              ║
║  4. Actualizar producto          ║
║  5. Eliminar producto            ║
║  6. Estadísticas                 ║
║  7. Guardar JSON                 ║
║  8. Cargar JSON                  ║
║  9. Salir                        ║
╚══════════════════════════════════╝
```

---

## 📋 Funcionalidades

### CRUD de productos

Cada producto en memoria se representa como un diccionario con las claves:

```python
{"nombre": str, "precio": float, "cantidad": int}
```

| Operación  | Descripción |
|------------|-------------|
| Agregar    | Valida que el nombre no exista antes de insertar |
| Mostrar    | Tabla con número, nombre, precio, cantidad y subtotal |
| Buscar     | Búsqueda insensible a mayúsculas, retorna datos o mensaje |
| Actualizar | Permite cambiar precio y/o cantidad (campos opcionales) |
| Eliminar   | Pide confirmación antes de borrar |

### Estadísticas

La opción 6 calcula y muestra:

- **Unidades totales** en stock
- **Valor total** del inventario
- **Producto más caro** (nombre y precio)
- **Producto con mayor stock** (nombre y cantidad)

El subtotal por producto se calcula con una función lambda:

```python
subtotal = lambda p: p["precio"] * p["cantidad"]
```

### Persistencia JSON

#### Guardar (opción 7)

Guarda el inventario en un archivo `.json` con el formato:

```json
{
    "1": {"nombre": "Laptop", "precio": 999.99, "cantidad": 5},
    "2": {"nombre": "Cuaderno", "precio": 2.0, "cantidad": 50}
}
```

- Valida que el inventario no esté vacío antes de escribir.
- Maneja errores de permisos y escritura sin cerrar el programa.

#### Cargar (opción 8)

Carga un archivo `.json` al inventario con validaciones por entrada:

- Claves `nombre`, `precio`, `cantidad` presentes y con tipos correctos.
- `precio` ≥ 0 y `cantidad` ≥ 0.
- Las entradas inválidas se omiten y se reporta cuántas hubo.

Al cargar, el usuario elige la política de integración:

| Opción | Comportamiento |
|--------|----------------|
| **S** (Sobrescribir) | Reemplaza completamente el inventario actual |
| **N** (Fusionar) | Si el nombre ya existe: suma cantidad y actualiza precio. Si es nuevo: lo agrega |

Al finalizar muestra un resumen: productos cargados, entradas inválidas y acción aplicada.

---

## 🧩 Módulos

### `servicios.py`

| Función | Descripción |
|---------|-------------|
| `agregar_producto(inventario, nombre, precio, cantidad)` | Agrega un producto; retorna `False` si ya existe |
| `mostrar_inventario(inventario)` | Imprime tabla formateada |
| `buscar_producto(inventario, nombre)` | Retorna el dict del producto o `None` |
| `actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)` | Actualiza campos opcionales |
| `eliminar_producto(inventario, nombre)` | Elimina por nombre |
| `calcular_estadisticas(inventario)` | Retorna dict con métricas o `None` si está vacío |
| `mostrar_estadisticas(inventario)` | Imprime estadísticas con formato |

### `archivos.py`

| Función | Descripción |
|---------|-------------|
| `guardar_json(inventario, ruta)` | Escribe el inventario en JSON |
| `cargar_json(ruta)` | Lee y valida el JSON; retorna lista o `None` |
| `cargar_e_integrar(inventario, ruta)` | Orquesta carga + pregunta de política al usuario |

### `app.py`

Contiene el bucle principal `main()`, los helpers de entrada (`pedir_float`, `pedir_int`, `pedir_nombre`) y las funciones de acción para cada opción del menú.

---

## 🛡️ Manejo de errores

- Ningún error del usuario cierra el programa.
- Entradas de texto donde se espera número: se repite la solicitud.
- Valores negativos: rechazados con mensaje.
- Archivo no encontrado, JSON malformado, error de codificación o permisos: mensaje claro y retorno al menú.
- `Ctrl+C` durante la ejecución: salida elegante sin traza de error.

---

## 👥 Autores

Proyecto académico — Programación con Python  
