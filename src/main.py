import pandas as pd


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