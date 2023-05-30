# requisito pip install psutil
import psutil
import shutil
import platform
import getpass
import socket

def mostrar_info_sistema():
    print("--- Información del sistema ---")
    print("Nombre del sistema: ", platform.node())
    print("Sistema operativo: ", platform.system())
    print("Versión del sistema operativo: ", platform.release())
    print("Nombre del usuario activo: ", getpass.getuser())
    print("Grupo de trabajo: ", socket.getfqdn())
    print("CPU: ", psutil.cpu_percent(interval=1), "%")
    print("Memoria RAM: ", psutil.virtual_memory().percent, "%")

def sizeof_fmt(num, suffix='B'):
    # Función auxiliar para formatear tamaños en bytes a una representación más legible
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

def mostrar_info_discos():
    print("--- Información del disco duro ---")
    discos = psutil.disk_partitions()
    for disco in discos:
        print("Disco: ", disco.device)
        print("Sistema de archivos: ", disco.fstype)
        
        # Obtener el tamaño total, usado y libre del disco
        espacio_total = psutil.disk_usage(disco.mountpoint).total
        espacio_usado = psutil.disk_usage(disco.mountpoint).used
        espacio_libre = psutil.disk_usage(disco.mountpoint).free
        
        # Formatear los tamaños para una mejor legibilidad
        espacio_total_fmt = sizeof_fmt(espacio_total)
        espacio_usado_fmt = sizeof_fmt(espacio_usado)
        espacio_libre_fmt = sizeof_fmt(espacio_libre)
        
        print("Espacio total: ", espacio_total_fmt)
        print("Espacio usado: ", espacio_usado_fmt)
        print("Espacio libre: ", espacio_libre_fmt)


def mostrar_info_memoria():
    print("--- Información de la memoria RAM ---")
    memoria = psutil.virtual_memory()
    print("Total: ", memoria.total / (1024**3), "GB")
    print("Disponible: ", memoria.available / (1024**3), "GB")
    print("Usada: ", memoria.used / (1024**3), "GB")
    print("Porcentaje utilizado: ", memoria.percent, "%")

def mostrar_info_cpu():
    print("--- Información de la CPU ---")
    # Mostrar porcentaje de uso de la CPU por núcleo
    for i, porcentaje in enumerate(psutil.cpu_percent(interval=1, percpu=True)):
        print("CPU", i, ": ", porcentaje, "%")
    # Mostrar porcentaje promedio de uso de la CPU
    print("Promedio de uso de la CPU: ", psutil.cpu_percent(interval=1), "%")

def mostrar_info_red():
    print("--- Información de la red ---")
    # Obtener estadísticas de la red
    estadisticas = psutil.net_io_counters()
    print("Bytes enviados: ", estadisticas.bytes_sent)
    print("Bytes recibidos: ", estadisticas.bytes_recv)

def mostrar_info_procesos():
    print("--- Información de los procesos en ejecución ---")
    # Obtener una lista de procesos
    procesos = psutil.process_iter()
    for proceso in procesos:
        try:
            nombre = proceso.name()
            pid = proceso.pid
            uso_cpu = proceso.cpu_percent(interval=0.1)
            uso_memoria = proceso.memory_percent()
            print("Proceso: ", nombre)
            print("PID: ", pid)
            print("Uso de CPU: ", uso_cpu, "%")
            print("Uso de memoria: ", uso_memoria, "%")
            print("--------------------")
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

def mostrar_info_sistema_archivos():
    print("--- Información del sistema de archivos ---")
    particiones = psutil.disk_partitions(all=True)
    for particion in particiones:
        print("Dispositivo: ", particion.device)
        print("Punto de montaje: ", particion.mountpoint)
        print("Tipo de sistema de archivos: ", particion.fstype)
        print("Opciones de montaje: ", particion.opts)
        try:
            total, usado, libre = shutil.disk_usage(particion.mountpoint)
            print("Espacio total: ", total / (1024**3), "GB")
            print("Espacio usado: ", usado / (1024**3), "GB")
            print("Espacio libre: ", libre / (1024**3), "GB")
        except PermissionError:
            print("No se puede acceder a la información del espacio en disco.")
        print("--------------------")


def matar_proceso():
    pid = input("Escribe el PID del proceso a matar: ")
    try:
        proceso = psutil.Process(int(pid))
        proceso.kill()
        print("Proceso con PID", pid, "eliminado.")
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        print("No se pudo eliminar el proceso.")

# Función principal del programa
def main():
    while True:
        print("\n--- Menú ---")
        print("1. Mostrar información del sistema")
        print("2. Mostrar información del disco duro")
        print("3. Mostrar información de la memoria RAM")
        print("4. Mostrar información de la CPU")
        print("5. Mostrar información de la red")
        print("6. Mostrar información de los procesos en ejecución")
        print("7. Matar proceso en ejecución")
        print("8. Mostrar información del sistema de archivos")
        print("9. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            mostrar_info_sistema()
        elif opcion == "2":
            mostrar_info_discos()
        elif opcion == "3":
            mostrar_info_memoria()
        elif opcion == "4":
            mostrar_info_cpu()
        elif opcion == "5":
            mostrar_info_red()
        elif opcion == "6":
            mostrar_info_procesos()
        elif opcion == "7":
            matar_proceso()
        elif opcion == "8":
            mostrar_info_sistema_archivos()
        elif opcion == "9":
            break
        else:
            print("Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    main()