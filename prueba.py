import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns

#carga el dataframe
df_est=pd.read_csv("datos_estudiantes.csv")
#mostrar los primeros 5 registros
print(df_est.head())

#variable cualitativa nominal nombre de las carreras
frec_cualita=df_est["carrera"].value_counts().reset_index()
#renombrar columnas
frec_cualita.columns=["carrera","fi"]
#frecuencia relativa
frec_cualita["hi"]=frec_cualita["fi"]/len(df_est)
#frecuencia relativa porcentual
frec_cualita["hip"]=frec_cualita["hi"]*100
#frecuencia acumulada
frec_cualita["Fi"]=frec_cualita["fi"].cumsum()
#frecuencia relativa acumulada
frec_cualita["Hi"]=frec_cualita["hi"].cumsum()
print("TABLA DE FRECUENCIAS: CARRERAS")
print(frec_cualita)

# 1. Conteo de frecuencias para la variable discreta 'materias_aprobadas'
tabla_discreta = df_est['materias_aprobadas'].value_counts().sort_index().reset_index()

# 2. Renombramos las columnas para que coincidan con tu Guía Metodológica
tabla_discreta.columns = ['Materias_X', 'fi']
#calculo de Frecuencia relativa
tabla_discreta['hi']=tabla_discreta['fi']/len(df_est)
# 3. Cálculo de Frecuencias Acumuladas (Fi)
# El método .cumsum() realiza la suma sucesiva que explicaste en el PDF
tabla_discreta['Fi'] = tabla_discreta['fi'].cumsum()
tabla_discreta['Hi']=tabla_discreta['hi'].cumsum()
tabla_discreta['hip']=tabla_discreta['hi']*100

print("TABLA DE FRECUENCIAS: MATERIAS APROBADAS")
print(tabla_discreta)

#TABLA DE FRECUENCIAS PARA LA VARIABLE CUANTITATIVA DISCRETA EDAD
n = len(df_est)
rango = df_est['edad'].max() - df_est['edad'].min()

# Aplicación de la Regla de Sturges (Rigor académico)
#ceil redondea hacia arriba
k = int(np.ceil(1 + 3.322 * np.log10(n)))
amplitud = rango / k
print(f"n: {n}, Rango: {rango}, Intervalos (k): {k}, Amplitud: {amplitud}")
#divide el rango en k partes en tipo array
cortes=np.arange(df_est["edad"].min(),df_est["edad"].max()+amplitud,amplitud)

#Definicion de intervalos
#include_lowest=True incluye el primer intervalo
#right=False indica que el intervalo es [a,b)
df_est["intervalos"]=pd.cut(df_est["edad"],bins=cortes,include_lowest=True,right=False)
#a partir de los intervalos se cuentan las frecuencias
tabla_agrupada=df_est["intervalos"].value_counts().sort_index().reset_index()
tabla_agrupada.columns=["intervalos","fi"]
#nos permite calcular la media de los intervalos
#lambda se usa para aplicar una funcion a cada elemento de la columna
tabla_agrupada["marca_clase"]=tabla_agrupada["intervalos"].apply(lambda x: x.mid)
#frecuencia relativa
tabla_agrupada["hi"]=tabla_agrupada["fi"]/len(df_est)
#frecuencia relativa porcentual
tabla_agrupada["hip"]=tabla_agrupada["hi"]*100
#frecuencia acumulada
tabla_agrupada["Fi"]=tabla_agrupada["fi"].cumsum()
#frecuencia relativa acumulada
tabla_agrupada["Hi"]=tabla_agrupada["hi"].cumsum()
print(tabla_agrupada)

#FASE de representacion grafica
# Configuración de estilo académico
# Permite que los gráficos se dibujen directamente debajo de la celda (exclusivo para cuadernos)
# 'style.use' define el "tema" visual.
# 'seaborn-v0_8-whitegrid' pone un fondo blanco con una rejilla (grid) gris clara.
# La rejilla es fundamental para que el ojo pueda seguir la línea del eje hacia el dato.
plt.style.use('seaborn-v0_8-whitegrid')
# Configuramos tamaños de fuente para que el usuario pueda leer bien las etiquetas
plt.rcParams['axes.titlesize'] = 16 # Tamaño del título principal
plt.rcParams['axes.labelsize'] = 12 # Tamaño de los nombres en los ejes X e Y

# fig: Es el objeto "Figura". Imaginalo como la ventana o el marco del cuadro.
# ax: Es el objeto "Axes". Es el lienzo real donde se pintan los datos.
# figsize=(12, 6): Define el tamaño. El primer número es el ANCHO y el segundo el ALTO.
# Se mide en pulgadas. Si lo aumentas, el gráfico se hace más grande en tu pantalla.
fig,ax=plt.subplots(figsize=(12,6))

# .hist(): Dibuja el Histograma (barras unidas).
ax.hist(df_est['edad'], bins=cortes, color='#11caa0', edgecolor='white', alpha=0.6, label='Histograma')

# CORRECCIÓN: Se cambió 'df_edad' por 'tabla_agrupada' para que use tus datos reales
ax.plot(tabla_agrupada['marca_clase'], tabla_agrupada['fi'], color='red', marker='D', linewidth=2, label='Polígono')

ax.set_title('ANÁLISIS DE DISTRIBUCIÓN DE EDADES (DATOS AGRUPADOS)', fontweight='bold')
# set_xticks(cortes): Obliga al eje X a mostrar exactamente los límites de tus intervalos.
ax.set_xticks(cortes)
ax.set_xlabel('Intervalos de Clase (años) / Marca de Clase (Xi)')
ax.set_ylabel('Frecuencia Absoluta (fi)')

# .legend(): Muestra el cuadro explicativo de las etiquetas
ax.legend()
plt.show()

