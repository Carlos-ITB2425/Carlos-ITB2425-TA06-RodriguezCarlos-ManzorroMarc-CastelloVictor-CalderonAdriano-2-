# -*- coding: utf-8 -*-

import os
import pandas as pd
from datetime import datetime


def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or (año % 400 == 0)


def inicializar_logs():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_errores = open(f"log_errores_{timestamp}.txt", "w", encoding='utf-8')
    log_valores = open(f"Datos_{timestamp}.log", "w", encoding='utf-8')
    log_final = open(f"resultados_finales_{timestamp}.log", "w", encoding='utf-8')
    return log_errores, log_valores, log_final, timestamp


def procesar_archivo(directorio, archivo, log_errores, log_valores):
    datos = []
    ruta_archivo = os.path.join(directorio, archivo)
    partes_nombre = archivo.split('.')
    if len(partes_nombre) < 3:
        log_errores.write(f"Error en {archivo}: Nombre del archivo no tiene el formato esperado.\n")
        return datos

    identificador_esperado = partes_nombre[1]
    with open(ruta_archivo, 'r', encoding='utf-8') as file:
        for numero_linea, linea in enumerate(file, start=1):
            partes = linea.strip().split()
            if len(partes) < 34:
                log_errores.write(f"Error en {archivo}: Línea {numero_linea} no tiene suficientes campos.\n")
                continue

            identificador = partes[0]
            if identificador != identificador_esperado:
                log_errores.write(
                    f"Error en {archivo}: Línea {numero_linea} tiene un identificador incorrecto ({identificador}).\n")
                continue

            try:
                año = int(partes[1])
                mes = int(partes[2])
                precipitaciones = list(map(float, partes[3:]))
                for dia, precipitacion in enumerate(precipitaciones, start=1):
                    datos.append((año, mes, dia, precipitacion))
                    log_valores.write(f"{año}-{mes:02d}-{dia:02d}: {precipitacion}\n")
            except ValueError as e:
                log_errores.write(f"Error en {archivo}: Línea {numero_linea} contiene valores no numéricos. {e}\n")
                continue
    return datos


def analizar_archivos(directorio):
    print("Ejecución iniciada...")
    log_errores, log_valores, log_final, timestamp = inicializar_logs()
    archivos = [f for f in os.listdir(directorio) if f.endswith(".dat")]
    total_archivos = len(archivos)
    total_lineas_procesadas = 0

    all_datos = []
    for archivo in archivos:
        datos_archivo = procesar_archivo(directorio, archivo, log_errores, log_valores)
        total_lineas_procesadas += len(datos_archivo)
        all_datos.extend(datos_archivo)

    df = pd.DataFrame(all_datos, columns=['Año', 'Mes', 'Día', 'Precipitación'])
    df = df.drop_duplicates(subset=['Año', 'Mes', 'Día'])
    datos_totales = len(df)
    datos_faltantes = (df['Precipitación'] == -999).sum()
    porcentaje_faltantes = (datos_faltantes / datos_totales) * 100

    df['Precipitación'] = df['Precipitación'].replace(-999, pd.NA)
    precipitacion_anual = df.groupby('Año')['Precipitación'].sum()
    cambio_anual = precipitacion_anual.pct_change().fillna(0) * 100

    log_final.write(f"Ejecución: {timestamp}\n")
    log_final.write(f"Total de valores procesados: {datos_totales}\n")
    log_final.write(f"Número de valores restantes (-999): {datos_faltantes}\n")
    log_final.write(f"Porcentaje de datos restantes: {porcentaje_faltantes:.2f}%\n")
    log_final.write(f"Archivos procesados: {total_archivos}\n")
    log_final.write(f"Líneas procesadas: {total_lineas_procesadas}\n")
    log_final.write("\nPrecipitación total anual:\n")
    log_final.write(precipitacion_anual.to_string())
    log_final.write("\n\nTasa de variación anual de precipitaciones (%):\n")
    log_final.write(cambio_anual.to_string())

    log_errores.close()
    log_valores.close()
    log_final.close()
    print("¡Ejecución finalizada!")


# Ejecutar el análisis para el directorio especificado
directorio = "Prueba"
analizar_archivos(directorio)
