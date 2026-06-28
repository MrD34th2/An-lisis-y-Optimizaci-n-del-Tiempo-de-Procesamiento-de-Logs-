"""generar_logs.py Genera un archivo de logs simulado para pruebas."""
import random
 
NIVELES = ["INFO", "WARNING", "ERROR", "DEBUG"]
MENSAJES = [
    "Conexion establecida con la base de datos",
    "Solicitud HTTP recibida en /api/usuarios",
    "Timeout al conectar con el servicio externo",
    "Autenticacion fallida para el usuario admin",
    "Archivo de configuracion cargado correctamente",
    "Memoria disponible por debajo del umbral",
    "Proceso de respaldo iniciado",
    "Error al escribir en disco: espacio insuficiente",
    "Sesion de usuario cerrada correctamente",
    "Respuesta enviada con codigo 200",
    "Respuesta enviada con codigo 404",
    "Respuesta enviada con codigo 500",
    "Cache invalidada correctamente",
    "Nuevo hilo de ejecucion iniciado",
    "Conexion cerrada por inactividad",
]
 
def generar_logs(nombre_archivo="logs.txt", cantidad=10000):
    with open(nombre_archivo, "w", encoding="utf-8") as f:
        for i in range(1, cantidad + 1):
            nivel = random.choice(NIVELES)
            mensaje = random.choice(MENSAJES)
            linea = f"[2024-06-{random.randint(1,30):02d} {random.randint(0,23):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}] [{nivel}] {mensaje}\n"
            f.write(linea)
    print(f"Archivo '{nombre_archivo}' generado con {cantidad} lineas.")
 
if __name__ == "__main__":
    generar_logs()
 