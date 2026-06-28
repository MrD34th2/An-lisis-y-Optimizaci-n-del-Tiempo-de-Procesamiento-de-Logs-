"""
version_optimizada.py
Version OPTIMIZADA del procesador de logs.
Recorre el archivo UNA sola vez y recopila todo en simultaneo.
"""
import time
import os

def procesar_logs_optimizado(nombre_archivo="logs.txt"):
    inicio = time.perf_counter()
    conteo = {"INFO": 0, "WARNING": 0, "ERROR": 0, "DEBUG": 0}
    mensajes_error = []
    total_lineas = 0
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            total_lineas += 1
            if   "[INFO]" in linea:    conteo["INFO"] += 1
            elif "[WARNING]" in linea: conteo["WARNING"] += 1
            elif "[ERROR]" in linea:   conteo["ERROR"] += 1; mensajes_error.append(linea)
            elif "[DEBUG]" in linea:   conteo["DEBUG"] += 1
    fin = time.perf_counter()
    return {
        "version": "optimizada",
        "total_lineas": total_lineas,
        "INFO": conteo["INFO"], "WARNING": conteo["WARNING"], "ERROR": conteo["ERROR"],
        "mensajes_error": len(mensajes_error),
        "tiempo_ms": round((fin - inicio) * 1000, 4),
    }

if __name__ == "__main__":
    r = procesar_logs_optimizado()
    print(f"\n=== VERSION OPTIMIZADA ===")
    print(f"  Lineas procesadas: {r['total_lineas']}")
    print(f"  INFO: {r['INFO']}  WARNING: {r['WARNING']}  ERROR: {r['ERROR']}")
    print(f"  Tiempo: {r['tiempo_ms']} ms")