import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency
import folium
from folium.plugins import MarkerCluster
import os

df = pd.read_csv('../data/Airbnb_Open_Data.csv')

print("--------IMPRIMIMOS LOS DATOS Y COLUMNAS---------")
print(df.head())
print(df.columns)


print("--------IMPRIMIMOS LOS DATOS Y COLUMNAS---------")

desc = pd.DataFrame(index = list(df))
desc['count'] = df.count()
desc['nunique'] = df.nunique()
desc['%unique'] = desc['nunique'] / len(df) * 100
desc['null'] = df.isnull().sum()
desc['%null'] = desc['null'] / len(df) * 100
desc['type'] = df.dtypes
desc = pd.concat([desc, df.describe().T.drop('count', axis = 1)], axis = 1)
print(desc)


# Eliminamos las columnas innecesarias
df.drop(columns=['NAME','license','country','country code'],inplace=True)

# Manipulamos y eliminamos los registros con valores faltantes
df['price'] = df['price'].str.replace(',', '', regex=True).str[1:-1].apply(lambda x: int(x) if pd.notna(x) else np.nan)
df['service fee'] = df['service fee'].str.replace(',', '', regex=True).str[1:-1].apply(lambda x: int(x) if pd.notna(x) else np.nan)
df['last review'] = pd.to_datetime(df['last review'], errors='coerce')
df['host name'] = df['host name'].fillna('not available')
df['house_rules'] = df['house_rules'].fillna('not available')
cat_columns = ['host_identity_verified','instant_bookable','room type','cancellation_policy','neighbourhood group'
              ,'review rate number','Construction year']
num_columns = ['lat','long','minimum nights','number of reviews','reviews per month','price','service fee'
              ,'calculated host listings count','availability 365']
df = df.dropna(subset=['neighbourhood group'])
df = df.dropna(subset=['lat'])
df = df.dropna(subset=['long'])
df['neighbourhood group'] = df['neighbourhood group'].replace('manhatan', 'Manhattan')
df['neighbourhood group'] = df['neighbourhood group'].replace('brookln', 'Brooklyn')

cat_df = df[cat_columns]

# Chi-cuadrado y tabla de contingencia
chi2_contingency_table = pd.DataFrame(index=cat_columns, columns=cat_columns, dtype=float)

for col1 in cat_columns:
    for col2 in cat_columns:
        if col1 == col2:
            chi2_contingency_table.loc[col1, col2] = 1.0
        else:
            contingency_table = pd.crosstab(cat_df[col1], cat_df[col2])
            chi2, _, _, _ = chi2_contingency(contingency_table)
            chi2_contingency_table.loc[col1, col2] = chi2


plt.figure(figsize=(8, 4))
sns.heatmap(chi2_contingency_table, annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Resultados del test Chi-Cuadrado para las variables categoricas")
ruta_grafico = os.path.join('../images', 'chi-cuadrado.png')
plt.savefig(ruta_grafico)

# Cuestiones referentes a las zonas geográficas:
    # ¿Cómo se distribuyen geográficamente las propiedades de Airbnb en la ciudad de Nueva York?

map_center = [df['lat'].mean(), df['long'].mean()]
mymap = folium.Map(location=map_center, zoom_start=10)

# Agregar marcadores para cada casa
marker_cluster = MarkerCluster().add_to(mymap)

for index, row in df.iterrows():
    folium.Marker([row['lat'], row['long']]).add_to(marker_cluster)

# Mostrar el mapa
mymap.save('mapa_de_casas.html')

    # ¿Se observan diferencias notables en precios y disponibilidad entre distintos vecindarios?

plt.figure(figsize=(8, 4))
sns.barplot(data=df, x='neighbourhood group', y='price', hue='room type')
plt.xlabel('neighbourhood group')
plt.ylabel('room type')
ruta_grafico = os.path.join('../images', 'room_borough.png')
plt.savefig(ruta_grafico)

# Características de alojamientos:
    # ¿Cuál es la distribución de tipos de propiedades?,¿ son casas enteras, habitaciones, pisos enteros,...?


# Visualizar la distribución de tipos de propiedades
plt.figure(figsize=(8, 6))
sns.countplot(x='room type', data=df, palette='viridis')
plt.title('Distribución de Tipos de Propiedades')
plt.xlabel('Tipo de Propiedad')
plt.ylabel('Cantidad')
ruta_grafico = os.path.join('../images', 'distribucion.png')
plt.savefig(ruta_grafico)

    # ¿Cómo afectan las características de los alojamientos en el precio?

# Visualizar los precios según el tipo de alojamiento
plt.figure(figsize=(10, 6))
sns.barplot(x='room type', y='price', data=df, palette='viridis')
plt.title('Precios según el Tipo de Alojamiento')
plt.xlabel('Tipo de Alojamiento')
plt.ylabel('Precio')
ruta_grafico = os.path.join('../images', 'precio_distribucion.png')
plt.savefig(ruta_grafico)

#  Calificaciones:
    # ¿Cómo se distribuyen las calificaciones de las revisiones?
plt.figure(figsize=(8, 6))
sns.histplot(df['review rate number'], bins=10, kde=True, color='skyblue')
plt.title('Distribución de Calificaciones de Revisiones')
plt.xlabel('Calificación de la Revisión')
plt.ylabel('Frecuencia')
ruta_grafico = os.path.join('../images', 'calificaciones.png')
plt.savefig(ruta_grafico)

#
plt.figure(figsize=(10, 6))
sns.countplot(x='review rate number', data=df, palette='viridis')
plt.title('Frecuencia de Calificaciones de Revisiones')
plt.xlabel('Calificación de la Revisión')
plt.ylabel('Frecuencia')
ruta_grafico = os.path.join('../images', 'calificaciones2.png')
plt.savefig(ruta_grafico)
    # ¿Hay correlaciones entre las diferentes categorías de calificaciones y el precio?
plt.figure(figsize=(10, 6))
sns.barplot(x='review rate number', y='price', data=df, palette='viridis')
plt.title('Precios según la Calificacion')
plt.xlabel('Tipo de Alojamiento')
plt.ylabel('Precio')
ruta_grafico = os.path.join('../images', 'precio_calificacion.png')
plt.savefig(ruta_grafico)


# Política de Cancelación:

plt.figure(figsize=(10, 6))
sns.boxplot(x='cancellation_policy', y='price', data=df, palette='Set3')
plt.title('Relación entre Precios y Política de Cancelación')
plt.xlabel('Política de Cancelación')
plt.ylabel('Precio')
ruta_grafico = os.path.join('../images', 'precio_cancelacion.png')
plt.savefig(ruta_grafico)