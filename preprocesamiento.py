import pandas as pd

# Cargar datos desde un CSV
df = pd.read_csv('data.csv')  # Reemplaza con tu ruta de archivo

# Mostrar las primeras filas
display(df.head())

# Revisar información general del DataFrame
df.info()

# Revisar valores nulos por columna
print(df.isnull().sum())

# Eliminar filas con valores nulos
df_cleaned = df.dropna()

# Rellenar valores nulos con la media de la columna
df_filled = df.fillna(df.mean(numeric_only=True))

# Renombrar columnas
df_renamed = df.rename(columns={'old_name': 'new_name'})

# Crear una nueva columna
df['new_column'] = df['existing_column'] * 2

# Filtrar datos
df_filtered = df[df['column_name'] > 100]

# Agrupar datos y calcular métricas
df_grouped = df.groupby('category_column')['numeric_column'].mean().reset_index()

# Merge con otro DataFrame
df2 = pd.read_csv('data2.csv')  # Otro archivo de datos
df_merged = df.merge(df2, on='common_column', how='inner')

# Guardar el DataFrame procesado a un nuevo CSV
df_merged.to_csv('processed_data.csv', index=False)

print("Procesamiento completado y datos guardados en 'processed_data.csv'")