"""
archivos.py
Módulo para persistencia del inventario en archivos JSON.

Formato en disco:
{
    "1": {"nombre": "...", "precio": 0.0, "cantidad": 0},
    "2": {...},
    ...
}
Las claves son strings numéricos ("1", "2", ...) como en el ejemplo del curso.
"""

import json
import os


# ──────────────────────────────────────────────
# GUARDAR JSON
# ──────────────────────────────────────────────

def guardar_json(inventario, ruta):
    """
    Guarda el inventario en un archivo JSON.

    El inventario (lista de dicts) se convierte a un dict con claves
    numéricas tipo string: {"1": {...}, "2": {...}, ...}

    Parámetros:
        inventario (list): Lista de dicts con productos.
        ruta (str): Ruta del archivo de destino (ej: 'inventario.json').

    Retorna:
        bool: True si se guardó correctamente, False en caso de error.
    """
    if not inventario:
        print("  ⚠  El inventario está vacío. No hay nada que guardar.")
        return False

    # Convertir lista → dict con claves "1", "2", ...
    datos = {
        str(i + 1): producto
        for i, producto in enumerate(inventario)
    }

    try:
        with open(ruta, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4, ensure_ascii=False)

        print(f"  ✔  Inventario guardado en: {os.path.abspath(ruta)}")
        return True

    except PermissionError:
        print(f"  ✖  Sin permisos para escribir en '{ruta}'. Verifique la ruta.")
    except OSError as e:
        print(f"  ✖  Error al guardar el archivo: {e}")

    return False


# ──────────────────────────────────────────────
# CARGAR JSON
# ──────────────────────────────────────────────

def cargar_json(ruta):
    """
    Lee un archivo JSON y retorna una lista de productos válidos.

    Valida que cada entrada tenga las claves 'nombre', 'precio' y 'cantidad'
    con los tipos correctos y valores no negativos.
    Las entradas inválidas se omiten y se reporta cuántas hubo.

    Parámetros:
        ruta (str): Ruta del archivo JSON a leer.

    Retorna:
        list | None:
            Lista de dicts {'nombre', 'precio', 'cantidad'} con entradas válidas,
            o None si ocurrió un error crítico.
    """
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            datos = json.load(f)

    except FileNotFoundError:
        print(f"  ✖  Archivo no encontrado: '{ruta}'")
        return None
    except json.JSONDecodeError as e:
        print(f"  ✖  El archivo no es un JSON válido: {e}")
        return None
    except UnicodeDecodeError:
        print(f"  ✖  Error de codificación al leer '{ruta}'. Use UTF-8.")
        return None
    except Exception as e:
        print(f"  ✖  Error inesperado al leer '{ruta}': {e}")
        return None

    # Validar que el contenido sea un dict
    if not isinstance(datos, dict):
        print("  ✖  Formato inválido: se esperaba un objeto JSON con claves numéricas.")
        return None

    productos = []
    entradas_invalidas = 0

    for clave, entrada in datos.items():
        try:
            if not isinstance(entrada, dict):
                raise ValueError("La entrada no es un objeto JSON")

            nombre = str(entrada.get("nombre", "")).strip()
            if not nombre:
                raise ValueError("Nombre vacío o ausente")

            precio = float(entrada["precio"])
            if precio < 0:
                raise ValueError("Precio negativo")

            cantidad = int(entrada["cantidad"])
            if cantidad < 0:
                raise ValueError("Cantidad negativa")

            productos.append({
                "nombre": nombre,
                "precio": precio,
                "cantidad": cantidad,
            })

        except (ValueError, KeyError, TypeError) as e:
            entradas_invalidas += 1
            print(f"  ⚠  Entrada '{clave}' omitida ({e}): {entrada}")

    if entradas_invalidas:
        print(f"  ⚠  {entradas_invalidas} entrada(s) inválida(s) omitida(s).")

    return productos


# ──────────────────────────────────────────────
# INTEGRACIÓN: cargar con política sobrescribir/fusionar
# ──────────────────────────────────────────────

def cargar_e_integrar(inventario, ruta):
    """
    Carga un JSON y aplica la política elegida por el usuario
    (sobrescribir o fusionar) sobre el inventario en memoria.

    Política de fusión:
        - Si el nombre ya existe: suma cantidades y actualiza el precio al nuevo.
        - Si el nombre es nuevo: se agrega directamente.

    Parámetros:
        inventario (list): Lista de dicts en memoria (se modifica en lugar).
        ruta (str): Ruta del JSON a cargar.

    Retorna:
        bool: True si la operación concluyó, False si falló la carga.
    """
    productos_cargados = cargar_json(ruta)

    if productos_cargados is None:
        return False

    if not productos_cargados:
        print("  ℹ  El archivo no contiene productos válidos.")
        return False

    print(f"\n  Se encontraron {len(productos_cargados)} producto(s) válido(s) en el archivo.")
    print("  Política de fusión: nombre coincide → suma cantidad + actualiza precio.")

    while True:
        opcion = input("  ¿Sobrescribir inventario actual? (S/N): ").strip().upper()
        if opcion in ("S", "N"):
            break
        print("  ⚠  Ingrese S o N.")

    if opcion == "S":
        inventario.clear()
        inventario.extend(productos_cargados)
        accion = "reemplazo"
    else:
        # Fusionar por nombre
        mapa = {p["nombre"].lower(): p for p in inventario}
        nuevos = 0
        actualizados = 0

        for prod in productos_cargados:
            key = prod["nombre"].lower()
            if key in mapa:
                mapa[key]["cantidad"] += prod["cantidad"]
                mapa[key]["precio"] = prod["precio"]
                actualizados += 1
            else:
                inventario.append(prod)
                mapa[key] = prod
                nuevos += 1

        print(f"  ℹ  Fusión: {nuevos} nuevo(s) agregado(s), {actualizados} actualizado(s).")
        accion = "fusión"

    print(f"\n  ✔  Carga completada → acción: {accion} | "
          f"productos en inventario ahora: {len(inventario)}")
    return True
