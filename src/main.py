import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

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


# Drop unneccesary columns
df.drop(columns=['NAME','license','country','country code'],inplace=True)


df['price'] = df['price'].str.replace(',', '', regex=True).str[1:-1].apply(lambda x: int(x) if pd.notna(x) else np.nan)
df['service fee'] = df['service fee'].str.replace(',', '', regex=True).str[1:-1].apply(lambda x: int(x) if pd.notna(x) else np.nan)
df['last review'] = pd.to_datetime(df['last review'], errors='coerce')

# missing values
df.isnull().sum()

df['host name'] = df['host name'].fillna('not available')
df['house_rules'] = df['house_rules'].fillna('not available')
cat_columns = ['host_identity_verified','instant_bookable','room type','cancellation_policy','neighbourhood group'
              ,'review rate number','Construction year']
num_columns = ['lat','long','minimum nights','number of reviews','reviews per month','price','service fee'
              ,'calculated host listings count','availability 365']
df = df.dropna(subset=['neighbourhood group'])
df = df.dropna(subset=['lat'])
df = df.dropna(subset=['long'])

cat_df = df[cat_columns]
# from scipy.stats import chi2_contingency
# # Create a chi-squared contingency table
# chi2_contingency_table = pd.DataFrame(index=cat_columns, columns=cat_columns, dtype=float)
#
# for col1 in cat_columns:
#     for col2 in cat_columns:
#         if col1 == col2:
#             chi2_contingency_table.loc[col1, col2] = 1.0
#         else:
#             contingency_table = pd.crosstab(cat_df[col1], cat_df[col2])
#             chi2, _, _, _ = chi2_contingency(contingency_table)
#             chi2_contingency_table.loc[col1, col2] = chi2
#
# # Create a heatmap to visualize the chi-squared test results
# plt.figure(figsize=(8, 4))
# sns.heatmap(chi2_contingency_table, annot=True, fmt=".2f", cmap='coolwarm')
# plt.title("Chi-Squared Test Results for Categorical Variables")
# plt.show()




# Cuestiones referentes a las zonas geográficas:
    # ¿Cómo se distribuyen geográficamente las propiedades de Airbnb en la ciudad de Nueva York?

import folium
from folium.plugins import MarkerCluster









# import folium
# from folium.plugins import MarkerCluster
#
# Supongamos que tienes un DataFrame llamado 'df' con datos geográficos
# y una columna 'latitude' y 'longitude'

# Crear un mapa centrado en las coordenadas promedio
# map_center = [df['lat'].mean(), df['long'].mean()]
# mymap = folium.Map(location=map_center, zoom_start=10)
#
# # Agregar marcadores para cada casa
# marker_cluster = MarkerCluster().add_to(mymap)
#
# for index, row in df.iterrows():
#     folium.Marker([row['lat'], row['long']]).add_to(marker_cluster)
#
# # Mostrar el mapa
# mymap.save('mapa_de_casas.html')




    # ¿Se observan diferencias notables en precios y disponibilidad entre distintos vecindarios?

# plt.figure(figsize=(8, 4))
# sns.barplot(data=df, x='neighbourhood group', y='price', hue='room type')
# plt.xlabel('neighbourhood group')
# plt.ylabel('room type')
# plt.show()


# Características de alojamientos:
    # ¿Cuál es la distribución de tipos de propiedades?,¿ son casas enteras, habitaciones, pisos enteros,...?


# Visualizar la distribución de tipos de propiedades
# plt.figure(figsize=(8, 6))
# sns.countplot(x='room type', data=df, palette='viridis')
# plt.title('Distribución de Tipos de Propiedades')
# plt.xlabel('Tipo de Propiedad')
# plt.ylabel('Cantidad')
# plt.show()


    # ¿Cómo afectan las características de los alojamientos en el precio?

# Visualizar los precios según el tipo de alojamiento
# plt.figure(figsize=(10, 6))
# sns.barplot(x='room type', y='price', data=df, palette='viridis')
# plt.title('Precios según el Tipo de Alojamiento')
# plt.xlabel('Tipo de Alojamiento')
# plt.ylabel('Precio')
# plt.show()
    # ¿Cuántos anfitriones tienen la distinción de super anfitrión?

# el dataset no tiene la columna que lo inidca
    # ¿Hay una correlación entre el rating de la propiedad y si la casa es de un super anfitrión?
# el dataset no tiene la columna que lo inidca


#  Calificaciones:
    # ¿Cómo se distribuyen las calificaciones de las revisiones?
# plt.figure(figsize=(8, 6))
# sns.histplot(df['review rate number'], bins=20, kde=True, color='skyblue')
# plt.title('Distribución de Calificaciones de Revisiones')
# plt.xlabel('Calificación de la Revisión')
# plt.ylabel('Frecuencia')
# plt.show()

#
# plt.figure(figsize=(10, 6))
# sns.countplot(x='review rate number', data=df, palette='viridis')
# plt.title('Frecuencia de Calificaciones de Revisiones')
# plt.xlabel('Calificación de la Revisión')
# plt.ylabel('Frecuencia')
# plt.show()
    # ¿Hay correlaciones entre las diferentes categorías de calificaciones y el precio?

# Temporalidad:
    # ¿Existen patrones estacionales en los precios o en la ocupación de las propiedades?

# Visualizar patrones estacionales en los precios
# plt.figure(figsize=(12, 6))
# sns.lineplot(x=df.index, y='price', data=df, color='skyblue')
# plt.title('Patrones Estacionales en los Precios a lo Largo del Tiempo')
# plt.xlabel('Fecha')
# plt.ylabel('Precio')
# plt.show()


# Servicios de las propiedades:
    # ¿Cuáles son los servicios más comunes ofrecidos por los anfitriones?
    # ¿Existe una correlación entre la presencia de ciertos servicios y el precio?

# plt.figure(figsize=(10, 6))
# sns.boxplot(x='cancellation_policy', y='price', data=df, palette='Set3')
# plt.title('Relación entre Precios y Política de Cancelación')
# plt.xlabel('Política de Cancelación')
# plt.ylabel('Precio')
# plt.show()
#
# plt.figure(figsize=(10, 6))
# sns.barplot(x='cancellation_policy', y='price', data=df, palette='Set3', estimator=np.median)
# plt.title('Relación entre Precios y Política de Cancelación')
# plt.xlabel('Política de Cancelación')
# plt.ylabel('Precio Mediano')
# plt.show()


# Interactivo
import plotly.express as px

# Supongamos que tienes un DataFrame llamado 'df' con las columnas relevantes, incluyendo 'price' y 'cancellation_policy'
# Asegúrate de que estas columnas y los datos estén correctamente estructurados

# Crear un DataFrame de ejemplo
#
# # Crear el gráfico interactivo con Plotly
# fig = px.scatter(df, x='cancellation_policy', y='price', color='price', title='Relación entre Precios y Política de Cancelación',
#                  labels={'cancellation_policy': 'Política de Cancelación', 'price': 'Precio'})
# fig.update_layout(showlegend=False)  # Ocultar la leyenda del color para mejorar la visualización
#
# # Mostrar el gráfico interactivo
# fig.show()


# Crear el mapa interactivo con Plotly
fig = px.scatter_mapbox(df, lat='lat', lon='long', color='price', size='price',
                        color_continuous_scale='Viridis', size_max=15, zoom=10,
                        mapbox_style="carto-positron", title='Mapa Interactivo de Precios')
fig.update_layout(showlegend=False)  # Ocultar la leyenda del color para mejorar la visualización

# Mostrar el mapa interactivo
fig.show()