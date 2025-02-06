import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime


def analizar_archivos(directorio, output_csv, output_img):
    print("Ejecución iniciada...")

    # Obtener lista de archivos .dat en el directorio
    archivos = [f for f in os.listdir(directorio) if f.endswith(".dat")]

    all_datos = []

    for archivo in archivos:
        ruta_archivo = os.path.join(directorio, archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as file:
            for linea in file:
                partes = linea.strip().split()
                if len(partes) < 34:
                    continue  # Saltar líneas con datos incompletos
                try:
                    año = int(partes[1])
                    mes = int(partes[2])
                    precipitaciones = list(map(float, partes[3:]))
                    for dia, precipitacion in enumerate(precipitaciones, start=1):
                        all_datos.append((año, mes, dia, precipitacion))
                except ValueError:
                    continue  # Ignorar líneas con errores de conversión

    # Crear DataFrame
    df = pd.DataFrame(all_datos, columns=['Año', 'Mes', 'Día', 'Precipitación'])
    df = df.drop_duplicates()
    df['Precipitación'] = df['Precipitación'].replace(-999, pd.NA)

    # Calcular estadísticas
    precipitacion_anual = df.groupby('Año')['Precipitación'].sum()
    cambio_anual = precipitacion_anual.pct_change().fillna(0) * 100

    resumen = pd.DataFrame({
        "Año": precipitacion_anual.index,
        "Precipitacion_Total_mm": precipitacion_anual.values,
        "Cambio_Anual_%": cambio_anual.values
    })

    # Guardar CSV
    resumen.to_csv(output_csv, index=False)

    # Generar gráfico
    plt.figure(figsize=(10, 5))
    plt.plot(resumen["Año"], resumen["Precipitacion_Total_mm"], marker="o", linestyle="-", color="b",
             label="Total anual")
    plt.xlabel("Año")
    plt.ylabel("Precipitación (mm)")
    plt.title("Evolución de la Precipitación Total Anual")
    plt.legend()
    plt.grid(True)
    plt.savefig(output_img)
    plt.close()

    print("¡Ejecución finalizada! Resultados guardados en CSV y gráfico generado.")


# Configurar rutas de salida
directorio = "./precip.MIROC5.RCP60.2006-2100.SDSM_REJ"  # Modifica esto con tu directorio real
output_csv = ("../resultados_meteorologicos.csv")
output_img = "./grafico_precipitacion.png"

# Ejecutar análisis
analizar_archivos(directorio, output_csv, output_img)
