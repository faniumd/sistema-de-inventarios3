"""
app.py
Punto de entrada del sistema de inventario.
Presenta el menú principal e integra todos los módulos.
"""

from servicios import (
    agregar_producto,
    mostrar_inventario,
    buscar_producto,
    actualizar_producto,
    eliminar_producto,
    mostrar_estadisticas,
)
from archivos import guardar_json, cargar_e_integrar


# ──────────────────────────────────────────────
# HELPERS DE ENTRADA
# ──────────────────────────────────────────────

def pedir_float(mensaje):
    """
    Solicita al usuario un número flotante no negativo.

    Parámetros:
        mensaje (str): Texto del prompt.

    Retorna:
        float: Valor ingresado y validado.
    """
    while True:
        try:
            valor = float(input(mensaje))
            if valor < 0:
                print("  ⚠  El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("  ⚠  Ingrese un número válido.")


def pedir_int(mensaje):
    """
    Solicita al usuario un entero no negativo.

    Parámetros:
        mensaje (str): Texto del prompt.

    Retorna:
        int: Valor ingresado y validado.
    """
    while True:
        try:
            valor = int(input(mensaje))
            if valor < 0:
                print("  ⚠  El valor no puede ser negativo.")
            else:
                return valor
        except ValueError:
            print("  ⚠  Ingrese un número entero válido.")


def pedir_nombre(mensaje):
    """
    Solicita un nombre de producto no vacío.

    Parámetros:
        mensaje (str): Texto del prompt.

    Retorna:
        str: Nombre ingresado con espacios extremos eliminados.
    """
    while True:
        nombre = input(mensaje).strip()
        if nombre:
            return nombre
        print("  ⚠  El nombre no puede estar vacío.")


# ──────────────────────────────────────────────
# ACCIONES DEL MENÚ
# ──────────────────────────────────────────────

def accion_agregar(inventario):
    """Flujo completo para agregar un producto."""
    print("\n  ── Agregar producto ──")
    nombre   = pedir_nombre("  Nombre   : ")
    precio   = pedir_float("  Precio   : $")
    cantidad = pedir_int("  Cantidad : ")
    agregar_producto(inventario, nombre, precio, cantidad)


def accion_buscar(inventario):
    """Flujo para buscar e imprimir un producto."""
    print("\n  ── Buscar producto ──")
    nombre = pedir_nombre("  Nombre a buscar: ")
    producto = buscar_producto(inventario, nombre)
    if producto:
        print(f"\n  Encontrado → Nombre: {producto['nombre']} | "
              f"Precio: ${producto['precio']:.2f} | "
              f"Cantidad: {producto['cantidad']}")
    else:
        print(f"  ℹ  Producto '{nombre}' no encontrado.")


def accion_actualizar(inventario):
    """Flujo para actualizar precio y/o cantidad de un producto."""
    print("\n  ── Actualizar producto ──")
    nombre = pedir_nombre("  Nombre del producto a actualizar: ")

    if buscar_producto(inventario, nombre) is None:
        print(f"  ⚠  Producto '{nombre}' no encontrado.")
        return

    print("  Deje en blanco para mantener el valor actual.")

    # Precio
    entrada_precio = input("  Nuevo precio (Enter = sin cambio): $").strip()
    nuevo_precio = None
    if entrada_precio:
        try:
            nuevo_precio = float(entrada_precio)
            if nuevo_precio < 0:
                print("  ⚠  Precio negativo ignorado.")
                nuevo_precio = None
        except ValueError:
            print("  ⚠  Precio inválido ignorado.")

    # Cantidad
    entrada_cantidad = input("  Nueva cantidad (Enter = sin cambio): ").strip()
    nueva_cantidad = None
    if entrada_cantidad:
        try:
            nueva_cantidad = int(entrada_cantidad)
            if nueva_cantidad < 0:
                print("  ⚠  Cantidad negativa ignorada.")
                nueva_cantidad = None
        except ValueError:
            print("  ⚠  Cantidad inválida ignorada.")

    actualizar_producto(inventario, nombre, nuevo_precio, nueva_cantidad)


def accion_eliminar(inventario):
    """Flujo para eliminar un producto con confirmación."""
    print("\n  ── Eliminar producto ──")
    nombre = pedir_nombre("  Nombre del producto a eliminar: ")

    if buscar_producto(inventario, nombre) is None:
        print(f"  ⚠  Producto '{nombre}' no encontrado.")
        return

    confirmar = input(f"  ¿Confirmar eliminación de '{nombre}'? (S/N): ").strip().upper()
    if confirmar == "S":
        eliminar_producto(inventario, nombre)
    else:
        print("  ℹ  Eliminación cancelada.")


def accion_guardar(inventario):
    """Flujo para guardar el inventario en JSON."""
    print("\n  ── Guardar JSON ──")
    ruta = input("  Ruta del archivo (ej: inventario.json): ").strip()
    if not ruta:
        ruta = "inventario.json"
    guardar_json(inventario, ruta)


def accion_cargar(inventario):
    """Flujo para cargar un JSON e integrar al inventario."""
    print("\n  ── Cargar JSON ──")
    ruta = input("  Ruta del archivo JSON a cargar: ").strip()
    if not ruta:
        print("  ⚠  Ruta vacía. Operación cancelada.")
        return
    cargar_e_integrar(inventario, ruta)


# ──────────────────────────────────────────────
# MENÚ PRINCIPAL
# ──────────────────────────────────────────────

MENU = """
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
  ╚══════════════════════════════════╝"""

ACCIONES = {
    "1": accion_agregar,
    "2": lambda inv: mostrar_inventario(inv),
    "3": accion_buscar,
    "4": accion_actualizar,
    "5": accion_eliminar,
    "6": lambda inv: mostrar_estadisticas(inv),
    "7": accion_guardar,
    "8": accion_cargar,
}


def main():
    """Bucle principal del programa."""
    inventario = []  # Lista de dicts en memoria

    print("\n  Bienvenido al Sistema de Inventario.")

    while True:
        print(MENU)

        try:
            opcion = input("  Seleccione una opción (1-9): ").strip()
        except (EOFError, KeyboardInterrupt):
            # Salida elegante con Ctrl+C o fin de entrada
            print("\n\n  Programa finalizado.")
            break

        if opcion == "9":
            print("\n  ¡Hasta luego!\n")
            break
        elif opcion in ACCIONES:
            try:
                ACCIONES[opcion](inventario)
            except Exception as e:
                # Captura cualquier error inesperado sin cerrar el programa
                print(f"\n  ✖  Error inesperado: {e}\n  El programa continúa.")
        else:
            print("  ⚠  Opción inválida. Ingrese un número del 1 al 9.")


if __name__ == "__main__":
    main()
