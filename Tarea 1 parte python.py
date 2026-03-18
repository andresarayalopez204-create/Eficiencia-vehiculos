import pandas as pd
import numpy as np

# Leer archivo CSV
df = pd.read_csv("C:\\Users\\andre\\OneDrive - Estudiantes ITCR\\Andrés\\9no Semestre\\Energía y sus transformaciones\\Tarea 1\\Gasolina.CSV", header=2)

# Quitar filas donde no haya dato de tiempo
df = df[df["Time"].notna()].copy()

# -------------------------
# INCISO A: tiempo a segundos
# -------------------------
tiempo = pd.to_timedelta(df["Time"])
tiempo_s = tiempo.dt.total_seconds().to_numpy()

print("Array de tiempo en segundos:")
print(tiempo_s)
print("\nPrimeros 10 valores de tiempo:")
print(tiempo_s[:10])

# -------------------------
# INCISO B: rapidez a m/s
# -------------------------
velocidad_kmh = pd.to_numeric(df["Speed (km/h)"], errors="coerce")

# Si falta algún dato, se mantiene el último valor disponible
velocidad_kmh = velocidad_kmh.ffill()

velocidad_ms = (velocidad_kmh / 3.6).to_numpy()

print("\nArray de rapidez en m/s:")
print(velocidad_ms)
print("\nPrimeros 10 valores de rapidez:")
print(velocidad_ms[:10])

# -------------------------
# INCISO C: altura en metros
# -------------------------
altura_m = pd.to_numeric(df["Altitude (m)"], errors="coerce")

# Si falta algún dato, se mantiene el último valor disponible
altura_m = altura_m.ffill()

altura_m = altura_m.to_numpy()

print("\nArray de altura en metros:")
print(altura_m)
print("\nPrimeros 10 valores de altura:")
print(altura_m[:10])

# -------------------------
# INCISO D: distancia recorrida en cada intervalo
# -------------------------

dt = np.diff(tiempo_s)

# Regla del trapecio para cada intervalo
delta_s = 0.5 * (np.abs(velocidad_ms[:-1]) + np.abs(velocidad_ms[1:])) * dt

print("\nArray de distancia por intervalo en metros:")
print(delta_s)

print("\nPrimeros 10 valores de distancia por intervalo:")
print(delta_s[:10])

# -------------------------
# INCISO E: distancia acumulada
# -------------------------

distancia_acumulada = np.cumsum(delta_s)

print("\nArray de distancia acumulada:")
print(distancia_acumulada)

print("\nPrimeros 10 valores de distancia acumulada:")
print(distancia_acumulada[:10])

import matplotlib.pyplot as plt

# -------------------------
# INCISO F: GRÁFICOS
# -------------------------

plt.figure(figsize=(10,8))

plt.subplot(3,1,1)
plt.plot(tiempo_s, velocidad_ms)
plt.title("Rapidez vs Tiempo")
plt.ylabel("m/s")
plt.grid()

plt.subplot(3,1,2)
plt.plot(tiempo_s, altura_m)
plt.title("Altura vs Tiempo")
plt.ylabel("m")
plt.grid()

plt.subplot(3,1,3)
plt.plot(tiempo_s[1:], distancia_acumulada)
plt.title("Distancia acumulada vs Tiempo")
plt.xlabel("Tiempo (s)")
plt.ylabel("m")
plt.grid()

plt.tight_layout()
plt.show()

# -------------------------
# INCISO G: tabla resumen del trayecto
# -------------------------

# Tiempo total del viaje
tiempo_total_s = tiempo_s[-1] - tiempo_s[0]

# Distancia total recorrida
distancia_total_m = distancia_acumulada[-1]

# Rapidez promedio
rapidez_promedio_ms = np.mean(velocidad_ms)

# Rapidez máxima
rapidez_maxima_ms = np.max(velocidad_ms)

# Tiempo detenido
# Consideramos detenido cuando v = 0 m/s
tiempo_detenido_s = np.sum(velocidad_ms == 0)

# Desnivel positivo y negativo
delta_h = np.diff(altura_m)

desnivel_positivo_m = np.sum(delta_h[delta_h > 0])
desnivel_negativo_m = np.sum(np.abs(delta_h[delta_h < 0]))

# Tabla resumen
resumen = pd.DataFrame({
    "Magnitud": [
        "Tiempo total del viaje (s)",
        "Distancia total recorrida (m)",
        "Rapidez promedio (m/s)",
        "Rapidez máxima (m/s)",
        "Tiempo detenido (s)",
        "Desnivel positivo (m)",
        "Desnivel negativo (m)"
    ],
    "Valor": [
        tiempo_total_s,
        distancia_total_m,
        rapidez_promedio_ms,
        rapidez_maxima_ms,
        tiempo_detenido_s,
        desnivel_positivo_m,
        desnivel_negativo_m
    ]
})

print("\nTabla resumen del trayecto:")
print(resumen.to_string(index=False))