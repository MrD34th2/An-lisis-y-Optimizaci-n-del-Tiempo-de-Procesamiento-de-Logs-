import time
import csv
import os
 
from version_secuencial import procesar_logs_secuencial
from version_optimizada import procesar_logs_optimizado
from generar_logs import generar_logs
 
 
# ─────────────────────────────────────────────
# CONFIGURACIÓN DEL EXPERIMENTO
# ─────────────────────────────────────────────
ARCHIVO_LOGS      = "logs.txt"
ARCHIVO_RESULTADOS = "resultados.csv"
ARCHIVO_REPORTE   = "reporte.txt"
CANTIDAD_LINEAS   = 10000   # Tamaño del archivo de prueba
REPETICIONES      = 5       # Número de ejecuciones por versión
 
 
def guardar_csv(filas):
    """Guarda todos los resultados en un archivo CSV."""
    campos = ["ejecucion", "version", "total_lineas", "INFO",
              "WARNING", "ERROR", "mensajes_error", "tiempo_ms"]
 
    with open(ARCHIVO_RESULTADOS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for i, fila in enumerate(filas, start=1):
            writer.writerow({
                "ejecucion"      : i,
                "version"        : fila["version"],
                "total_lineas"   : fila["total_lineas"],
                "INFO"           : fila["INFO"],
                "WARNING"        : fila["WARNING"],
                "ERROR"          : fila["ERROR"],
                "mensajes_error" : fila["mensajes_error"],
                "tiempo_ms"      : fila["tiempo_ms"],
            })
    print(f"\n  → Resultados guardados en '{ARCHIVO_RESULTADOS}'")
 
 
def calcular_promedio(resultados, version):
    """Calcula el tiempo promedio de una versión."""
    tiempos = [r["tiempo_ms"] for r in resultados if r["version"] == version]
    if not tiempos:
        return 0
    return round(sum(tiempos) / len(tiempos), 4)
 
 
def calcular_mejora(prom_sec, prom_opt):
    """Calcula el porcentaje de mejora entre las dos versiones."""
    if prom_sec == 0:
        return 0
    return round(((prom_sec - prom_opt) / prom_sec) * 100, 2)
 
 
def guardar_reporte(resultados, prom_sec, prom_opt, mejora):
    """Guarda un reporte legible del experimento."""
    separador = "=" * 55
 
    lineas_reporte = [
        separador,
        "   REPORTE DEL EXPERIMENTO - ANÁLISIS DE LOGS",
        separador,
        f"  Archivo analizado    : {ARCHIVO_LOGS}",
        f"  Líneas en el archivo : {CANTIDAD_LINEAS:,}",
        f"  Repeticiones         : {REPETICIONES} por versión",
        "",
        "  TIEMPOS POR EJECUCIÓN (ms)",
        "-" * 55,
        f"  {'Ejec':<6} {'Versión':<15} {'Tiempo (ms)':>12}",
        "-" * 55,
    ]
 
    for i, r in enumerate(resultados, start=1):
        lineas_reporte.append(
            f"  {i:<6} {r['version']:<15} {r['tiempo_ms']:>12.4f}"
        )
 
    lineas_reporte += [
        "",
        "  RESUMEN COMPARATIVO",
        "-" * 55,
        f"  Promedio secuencial  : {prom_sec:>10.4f} ms",
        f"  Promedio optimizado  : {prom_opt:>10.4f} ms",
        f"  Mejora obtenida      : {mejora:>10.2f} %",
        "",
        "  VERIFICACIÓN DE HIPÓTESIS",
        "-" * 55,
    ]
 
    if mejora >= 30:
        lineas_reporte.append(
            f"  ✅ HIPÓTESIS CONFIRMADA: se logró una mejora del {mejora}%"
        )
        lineas_reporte.append(
            "     (supera el umbral mínimo del 30%)"
        )
    else:
        lineas_reporte.append(
            f"  ❌ HIPÓTESIS NO CONFIRMADA: mejora del {mejora}%"
        )
        lineas_reporte.append(
            "     (no alcanza el umbral mínimo del 30%)"
        )
 
    lineas_reporte.append(separador)
 
    with open(ARCHIVO_REPORTE, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas_reporte) + "\n")
 
    print(f"  → Reporte guardado en '{ARCHIVO_REPORTE}'")
 
 
def main():
    print("=" * 55)
    print("   EXPERIMENTO: ANÁLISIS DE LOGS")
    print("=" * 55)
 
    # 1. Generar archivo de logs si no existe
    if not os.path.exists(ARCHIVO_LOGS):
        print(f"\n[1/4] Generando '{ARCHIVO_LOGS}' con {CANTIDAD_LINEAS:,} líneas...")
        generar_logs(ARCHIVO_LOGS, CANTIDAD_LINEAS)
    else:
        print(f"\n[1/4] Archivo '{ARCHIVO_LOGS}' encontrado. Usando el existente.")
 
    # 2. Ejecutar versión secuencial N veces
    print(f"\n[2/4] Ejecutando versión SECUENCIAL ({REPETICIONES} veces)...")
    resultados_sec = []
    for i in range(1, REPETICIONES + 1):
        r = procesar_logs_secuencial(ARCHIVO_LOGS)
        resultados_sec.append(r)
        print(f"      Ejecución {i}: {r['tiempo_ms']} ms")
 
    # 3. Ejecutar versión optimizada N veces
    print(f"\n[3/4] Ejecutando versión OPTIMIZADA ({REPETICIONES} veces)...")
    resultados_opt = []
    for i in range(1, REPETICIONES + 1):
        r = procesar_logs_optimizado(ARCHIVO_LOGS)
        resultados_opt.append(r)
        print(f"      Ejecución {i}: {r['tiempo_ms']} ms")
 
    # 4. Calcular métricas y guardar resultados
    print("\n[4/4] Calculando métricas y guardando resultados...")
 
    todos = resultados_sec + resultados_opt
    prom_sec = calcular_promedio(todos, "secuencial")
    prom_opt = calcular_promedio(todos, "optimizada")
    mejora   = calcular_mejora(prom_sec, prom_opt)
 
    guardar_csv(todos)
    guardar_reporte(todos, prom_sec, prom_opt, mejora)
 
    # 5. Mostrar resumen en pantalla
    print("\n" + "=" * 55)
    print("   RESUMEN FINAL")
    print("=" * 55)
    print(f"  Promedio secuencial  : {prom_sec} ms")
    print(f"  Promedio optimizado  : {prom_opt} ms")
    print(f"  Mejora obtenida      : {mejora} %")
 
    if mejora >= 30:
        print(f"\n  ✅ HIPÓTESIS CONFIRMADA ({mejora}% >= 30%)")
    else:
        print(f"\n  ❌ HIPÓTESIS NO CONFIRMADA ({mejora}% < 30%)")
 
    print("=" * 55)
 
 
if __name__ == "__main__":
    main()