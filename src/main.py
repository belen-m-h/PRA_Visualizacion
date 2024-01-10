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

cat_df = df[cat_columns]
from scipy.stats import chi2_contingency
# Create a chi-squared contingency table
chi2_contingency_table = pd.DataFrame(index=cat_columns, columns=cat_columns, dtype=float)

for col1 in cat_columns:
    for col2 in cat_columns:
        if col1 == col2:
            chi2_contingency_table.loc[col1, col2] = 1.0
        else:
            contingency_table = pd.crosstab(cat_df[col1], cat_df[col2])
            chi2, _, _, _ = chi2_contingency(contingency_table)
            chi2_contingency_table.loc[col1, col2] = chi2

# Create a heatmap to visualize the chi-squared test results
plt.figure(figsize=(8, 4))
sns.heatmap(chi2_contingency_table, annot=True, fmt=".2f", cmap='coolwarm')
plt.title("Chi-Squared Test Results for Categorical Variables")
plt.show()




# Cuestiones referentes a las zonas geográficas:
    # ¿Cómo se distribuyen geográficamente las propiedades de Airbnb en la ciudad de Nueva York?

import folium
from folium.plugins import MarkerCluster


mapa = {
'Brooklyn':[40.6782,-73.9442],
'brookln':[40.6782,-73.9442],
'Manhattan':[40.7831,-73.9712],
'manhatan':[40.7831,-73.9712],
'Queens':[40.7282,-73.7949],
'Staten Island':[ 40.5795,-74.1502],
'Bronx':[ 40.8448,-73.8648],
}


# coord_mapping = dict(zip(df['neighbourhood group'], zip(df['latitude'], df['longitude'])))

# Añadir las columnas de latitud y longitud al DataFrame
# df['latitude'] = mapa[df['neighbourhood group']][0]
# df['longitude'] =  mapa[df['neighbourhood group']][1]

df['latitude'] = df['neighbourhood group'].map(lambda x: mapa.get(x, [None, None])[0])
df['longitude'] = df['neighbourhood group'].map(lambda x: mapa.get(x, [None, None])[1])


# Visualizar las longitudes con los nuevos campos
plt.figure(figsize=(10, 6))
plt.scatter(df['longitude'], df['latitude'], c='blue', marker='o', label='Neighbourhood Group')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Mapa de Longitudes con Nuevos Campos')
plt.legend()
plt.show()



import folium
from folium.plugins import MarkerCluster

# Supongamos que tienes un DataFrame llamado 'df' con datos geográficos
# y una columna 'latitude' y 'longitude'

# Crear un mapa centrado en las coordenadas promedio
map_center = [df['latitude'].mean(), df['longitude'].mean()]
mymap = folium.Map(location=map_center, zoom_start=10)

# Agregar marcadores para cada casa
marker_cluster = MarkerCluster().add_to(mymap)

for index, row in df.iterrows():
    folium.Marker([row['latitude'], row['longitude']]).add_to(marker_cluster)

# Mostrar el mapa
mymap.save('mapa_de_casas.html')




    # ¿Se observan diferencias notables en precios y disponibilidad entre distintos vecindarios?

plt.figure(figsize=(8, 4))
sns.barplot(data=df, x='neighbourhood group', y='price', hue='room type')
plt.xlabel('neighbourhood group')
plt.ylabel('room type')
plt.show()


# Características de alojamientos:
    # ¿Cuál es la distribución de tipos de propiedades?,¿ son casas enteras, habitaciones, pisos enteros,...?
    # ¿Cómo afectan las características de los alojamientos en el precio?
    # ¿Cuántos anfitriones tienen la distinción de super anfitrión?
    # ¿Hay una correlación entre el rating de la propiedad y si la casa es de un super anfitrión?

#  Calificaciones:
    # ¿Cómo se distribuyen las calificaciones de las revisiones?
    # ¿Hay correlaciones entre las diferentes categorías de calificaciones y el precio?

# Temporalidad:
    # ¿Existen patrones estacionales en los precios o en la ocupación de las propiedades?

# Servicios de las propiedades:
    # ¿Cuáles son los servicios más comunes ofrecidos por los anfitriones?
    # ¿Existe una correlación entre la presencia de ciertos servicios y el precio?
