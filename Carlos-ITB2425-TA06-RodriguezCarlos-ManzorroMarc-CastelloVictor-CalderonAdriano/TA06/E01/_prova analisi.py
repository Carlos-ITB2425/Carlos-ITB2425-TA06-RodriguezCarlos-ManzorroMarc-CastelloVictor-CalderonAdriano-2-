import os
import glob

# Configuración
ruta_archivos = './Prova'  # Cambia esto a la ruta de tus archivos
archivos = glob.glob(os.path.join(ruta_archivos, '*.txt'))  # Ajusta la extensión si es necesario

# Variables para almacenar datos
total_archivos = len(archivos)
archivos_leidos = 0
archivos_con_error = 0
precipitaciones_por_anio = {}
temperaturas_por_anio = {}
errores = []

# Procesar cada archivo
for archivo in archivos:
    try:
        with open(archivo, 'r') as f:
            lineas = f.readlines()
            for linea in lineas:
                # Supongamos que cada línea tiene el formato: Año, Temperatura, Precipitación
                año, temperatura, precipitacion = map(float, linea.strip().split(','))

                if año not in precipitaciones_por_anio:
                    precipitaciones_por_anio[año] = []
                    temperaturas_por_anio[año] = []

                precipitaciones_por_anio[año].append(precipitacion)
                temperaturas_por_anio[año].append(temperatura)

        archivos_leidos += 1
    except Exception as e:
        archivos_con_error += 1
        errores.append(f"Error al leer {archivo}: {str(e)}")

# Calcular medias y otros datos
medias_precipitaciones = {año: sum(datos) / len(datos) for año, datos in precipitaciones_por_anio.items()}
medias_temperaturas = {año: sum(datos) / len(datos) for año, datos in temperaturas_por_anio.items()}

año_mas_lluvioso = max(medias_precipitaciones, key=medias_precipitaciones.get)
año_mas_seco = min(medias_precipitaciones, key=medias_precipitaciones.get)

# Escribir Datos.log
with open('Datos.log', 'w') as f:
    f.write(f"Total de archivos: {total_archivos}\n")
    f.write(f"Archivos leídos correctamente: {archivos_leidos}\n")
    f.write(f"Archivos con errores: {archivos_con_error}\n")

# Escribir resultados.log
with open('resultados.log', 'w') as f:
    f.write("Medias de precipitaciones y temperaturas por año:\n")
    for año in sorted(medias_precipitaciones.keys()):
        f.write(
            f"Año {año}: Precipitación media = {medias_precipitaciones[año]:.2f}, Temperatura media = {medias_temperaturas[año]:.2f}\n")

    f.write(f"\nAño más lluvioso: {año_mas_lluvioso}\n")
    f.write(f"Año más seco: {año_mas_seco}\n")

# Escribir errores.txt
with open('errores.txt', 'w') as f:
    for error in errores:
        f.write(error + "\n")

print("Procesamiento completado. Revisa los archivos generados.")