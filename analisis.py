import os
import pandas as pd

# Rutas relativas
input_path = os.path.join("data", "sensores_industriales.csv")
output_dir = "resultados"
output_path = os.path.join(output_dir, "alertas.csv")

# Asegurar que la carpeta de salida existe
os.makedirs(output_dir, exist_ok=True)

# Cargar los datos
df = pd.read_csv(input_path)

print("="*50)
print("   RESULTADOS DEL ANÁLISIS DE SENSORES INDUSTRIALES")
print("="*50)

# 1. Cantidad de registros y de sensores distintos
total_registros = len(df)
sensores_unicos = df['id_sensor'].nunique()
print(f"\n1. Registros totales: {total_registros:,}")
print(f"   Sensores distintos: {sensores_unicos}")

# 2. Temperatura promedio de cada planta
promedio_planta = df.groupby('planta')['temperatura_c'].mean()
print("\n2. Temperatura promedio por planta (°C):")
for planta, temp in promedio_planta.items():
    print(f"   - {planta}: {temp:.2f} °C")

# 3. Temperatura máxima, identificando sensor y fecha
max_temp = df['temperatura_c'].max()
registros_max = df[df['temperatura_c'] == max_temp]

print(f"\n3. Temperatura máxima registrada: {max_temp} °C")
for _, row in registros_max.iterrows():
    print(f"   - Sensor: {row['id_sensor']} | Fecha/Hora: {row['fecha_hora']} | Planta: {row['planta']}")

# 4. Lecturas con temperatura mayor a 85 °C (Alertas)
df_alertas = df[df['temperatura_c'] > 85]
total_alertas = len(df_alertas)
print(f"\n4. Total de lecturas con alerta (> 85 °C): {total_alertas}")

# 5. Planta con más alertas de temperatura (Manejo de empates)
conteo_alertas = df_alertas['planta'].value_counts()
if not conteo_alertas.empty:
    max_alertas_count = conteo_alertas.max()
    plantas_top = conteo_alertas[conteo_alertas == max_alertas_count].index.tolist()
    print(f"\n5. Planta(s) con más alertas ({max_alertas_count} alertas): {', '.join(plantas_top)}")
else:
    print("\n5. No se registraron alertas.")

# 6. Exportar lecturas con alerta a resultados/alertas.csv
df_alertas.to_csv(output_path, index=False)
print(f"\n6. Archivo de alertas generado exitosamente en: '{output_path}'")
print("="*50)
