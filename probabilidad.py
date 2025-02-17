import numpy as np
import pandas as pd
import scipy.stats as stats

# Cargar datos desde un CSV
df = pd.read_csv('data.csv')

# Medidas de tendencia central
mean_value = df['numeric_column'].mean()
median_value = df['numeric_column'].median()
mode_value = df['numeric_column'].mode()[0]
print(f"Media: {mean_value}, Mediana: {median_value}, Moda: {mode_value}")

# Medidas de dispersión
std_dev = df['numeric_column'].std()
variance = df['numeric_column'].var()
range_value = df['numeric_column'].max() - df['numeric_column'].min()
print(f"Desviación estándar: {std_dev}, Varianza: {variance}, Rango: {range_value}")

# Distribuciones de probabilidad
distribution = stats.norm.fit(df['numeric_column'])
print(f"Media y desviación estándar de la distribución normal: {distribution}")

# Prueba de normalidad (Shapiro-Wilk)
shapiro_test = stats.shapiro(df['numeric_column'])
print(f"Prueba de Shapiro-Wilk: Estadístico={shapiro_test.statistic}, p-valor={shapiro_test.pvalue}")

# Correlación entre dos variables
correlation = df[['numeric_column1', 'numeric_column2']].corr()
print("Matriz de correlación:")
print(correlation)

# Prueba de hipótesis (t-test)
ttest_result = stats.ttest_ind(df['numeric_column1'], df['numeric_column2'], nan_policy='omit')
print(f"T-test: Estadístico={ttest_result.statistic}, p-valor={ttest_result.pvalue}")
