"""
version_secuencial.py
Version ORIGINAL (sin optimizar) del procesador de logs.
Realiza multiples recorridos del archivo (uno por cada operacion).
"""
import time
import os

def contar_por_nivel(lineas, nivel):
    conteo = 0
    for linea in lineas:
        if f"[{nivel}]" in linea:
            conteo += 1
    return conteo

def buscar_errores(lineas):
    errores = []
    for linea in lineas:
        if "[ERROR]" in linea:
            errores.append(linea.strip())
    return errores

def contar_total(lineas):
    total = 0
    for linea in lineas:
        if linea.strip() != "":
            total += 1
    return total

def procesar_logs_secuencial(nombre_archivo="logs.txt"):
    inicio = time.perf_counter()
    with open(nombre_archivo, "r", encoding="utf-8") as f:
        lineas = f.readlines()
    total        = contar_total(lineas)
    info         = contar_por_nivel(lineas, "INFO")
    warning      = contar_por_nivel(lineas, "WARNING")
    error        = contar_por_nivel(lineas, "ERROR")
    mens_error   = buscar_errores(lineas)
    fin = time.perf_counter()
    return {
        "version": "secuencial",
        "total_lineas": total,
        "INFO": info, "WARNING": warning, "ERROR": error,
        "mensajes_error": len(mens_error),
        "tiempo_ms": round((fin - inicio) * 1000, 4),
    }

if __name__ == "__main__":
    r = procesar_logs_secuencial()
    print(f"\n=== VERSION SECUENCIAL ===")
    print(f"  Lineas procesadas: {r['total_lineas']}")
    print(f"  INFO: {r['INFO']}  WARNING: {r['WARNING']}  ERROR: {r['ERROR']}")
    print(f"  Tiempo: {r['tiempo_ms']} ms")