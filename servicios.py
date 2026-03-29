"""
servicios.py
Módulo con operaciones CRUD y estadísticas del inventario.
El inventario es una lista de diccionarios con claves: nombre, precio, cantidad.
"""


# ──────────────────────────────────────────────
# CRUD
# ──────────────────────────────────────────────

def agregar_producto(inventario, nombre, precio, cantidad):
    """
    Agrega un nuevo producto al inventario.

    Parámetros:
        inventario (list): Lista de dicts con productos.
        nombre (str): Nombre del producto.
        precio (float): Precio unitario (>= 0).
        cantidad (int): Unidades en stock (>= 0).

    Retorna:
        bool: True si se agregó, False si el nombre ya existe.
    """
    # Verificar que no exista un producto con el mismo nombre
    if buscar_producto(inventario, nombre) is not None:
        print(f"  ⚠  El producto '{nombre}' ya existe. Use 'Actualizar' para modificarlo.")
        return False

    inventario.append({
        "nombre": nombre,
        "precio": float(precio),
        "cantidad": int(cantidad)
    })
    print(f"  ✔  Producto '{nombre}' agregado correctamente.")
    return True


def mostrar_inventario(inventario):
    """
    Imprime el inventario en formato tabla.

    Parámetros:
        inventario (list): Lista de dicts con productos.

    Retorna:
        None
    """
    if not inventario:
        print("  ℹ  El inventario está vacío.")
        return

    # Encabezado de la tabla
    print(f"\n  {'#':<5} {'Nombre':<25} {'Precio':>10} {'Cantidad':>10} {'Subtotal':>12}")
    print("  " + "─" * 65)

    # Subtotal con lambda (opcional, Task 3)
    subtotal = lambda p: p["precio"] * p["cantidad"]

    for i, producto in enumerate(inventario, start=1):
        print(
            f"  {i:<5} {producto['nombre']:<25} "
            f"${producto['precio']:>9.2f} "
            f"{producto['cantidad']:>10} "
            f"${subtotal(producto):>11.2f}"
        )

    print("  " + "─" * 65)
    print(f"  {'Total de productos en lista:':<42} {len(inventario)}\n")


def buscar_producto(inventario, nombre):
    """
    Busca un producto por nombre (insensible a mayúsculas).

    Parámetros:
        inventario (list): Lista de dicts con productos.
        nombre (str): Nombre a buscar.

    Retorna:
        dict | None: El dict del producto si se encuentra, None en caso contrario.
    """
    nombre_lower = nombre.strip().lower()
    for producto in inventario:
        if producto["nombre"].lower() == nombre_lower:
            return producto
    return None


def actualizar_producto(inventario, nombre, nuevo_precio=None, nueva_cantidad=None):
    """
    Actualiza precio y/o cantidad de un producto existente.

    Parámetros:
        inventario (list): Lista de dicts con productos.
        nombre (str): Nombre del producto a actualizar.
        nuevo_precio (float | None): Nuevo precio; None = sin cambio.
        nueva_cantidad (int | None): Nueva cantidad; None = sin cambio.

    Retorna:
        bool: True si se actualizó, False si no se encontró el producto.
    """
    producto = buscar_producto(inventario, nombre)
    if producto is None:
        print(f"  ⚠  Producto '{nombre}' no encontrado.")
        return False

    if nuevo_precio is not None:
        producto["precio"] = float(nuevo_precio)
    if nueva_cantidad is not None:
        producto["cantidad"] = int(nueva_cantidad)

    print(f"  ✔  Producto '{nombre}' actualizado correctamente.")
    return True


def eliminar_producto(inventario, nombre):
    """
    Elimina un producto del inventario por nombre.

    Parámetros:
        inventario (list): Lista de dicts con productos.
        nombre (str): Nombre del producto a eliminar.

    Retorna:
        bool: True si se eliminó, False si no se encontró.
    """
    producto = buscar_producto(inventario, nombre)
    if producto is None:
        print(f"  ⚠  Producto '{nombre}' no encontrado.")
        return False

    inventario.remove(producto)
    print(f"  ✔  Producto '{nombre}' eliminado correctamente.")
    return True


# ──────────────────────────────────────────────
# ESTADÍSTICAS
# ──────────────────────────────────────────────

def calcular_estadisticas(inventario):
    """
    Calcula métricas globales del inventario.

    Parámetros:
        inventario (list): Lista de dicts con productos.

    Retorna:
        dict con claves:
            unidades_totales (int)
            valor_total (float)
            producto_mas_caro (dict | None)
            producto_mayor_stock (dict | None)
        Retorna None si el inventario está vacío.
    """
    if not inventario:
        return None

    # Lambda para subtotal de cada producto
    subtotal = lambda p: p["precio"] * p["cantidad"]

    unidades_totales = sum(p["cantidad"] for p in inventario)
    valor_total = sum(subtotal(p) for p in inventario)
    producto_mas_caro = max(inventario, key=lambda p: p["precio"])
    producto_mayor_stock = max(inventario, key=lambda p: p["cantidad"])

    return {
        "unidades_totales": unidades_totales,
        "valor_total": valor_total,
        "producto_mas_caro": producto_mas_caro,
        "producto_mayor_stock": producto_mayor_stock,
    }


def mostrar_estadisticas(inventario):
    """
    Imprime las estadísticas del inventario de forma legible.

    Parámetros:
        inventario (list): Lista de dicts con productos.

    Retorna:
        None
    """
    stats = calcular_estadisticas(inventario)
    if stats is None:
        print("  ℹ  El inventario está vacío, no hay estadísticas que mostrar.")
        return

    caro = stats["producto_mas_caro"]
    stock = stats["producto_mayor_stock"]

    print("\n  ╔══════════════════════════════════════════╗")
    print("  ║         ESTADÍSTICAS DEL INVENTARIO      ║")
    print("  ╠══════════════════════════════════════════╣")
    print(f"  ║  Unidades totales en stock : {stats['unidades_totales']:>12}║")
    print(f"  ║  Valor total del inventario: ${stats['valor_total']:>11.2f}║")
    print(f"  ║  Producto más caro    :{caro['nombre'][:18]:<18}║")
    print(f"  ║    └─ Precio               : ${caro['precio']:>11.2f}║")
    print(f"  ║  Mayor stock         :{stock['nombre'][:18]:<18} ║")
    print(f"  ║    └─ Cantidad             : {stock['cantidad']:>12}║")
    print("  ╚══════════════════════════════════════════╝\n")
