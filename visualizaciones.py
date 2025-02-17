import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Cargar datos desde un CSV
df = pd.read_csv('data.csv')

# Histogramas
fig = px.histogram(df, x='numeric_column', nbins=30, title='Histograma con Plotly')
fig.show()

plt.figure(figsize=(8, 5))
plt.hist(df['numeric_column'], bins=30, edgecolor='black')
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma con Matplotlib')
plt.show()

# Boxplots
fig = px.box(df, x='category_column', y='numeric_column', title='Boxplot con Plotly')
fig.show()

plt.figure(figsize=(8, 5))
sns.boxplot(x=df['category_column'], y=df['numeric_column'])
plt.xlabel('Categoría')
plt.ylabel('Valor')
plt.title('Boxplot con Matplotlib')
plt.show()

# Scatter Plots
fig = px.scatter(df, x='numeric_column1', y='numeric_column2', color='category_column', title='Scatter Plot con Plotly')
fig.show()

plt.figure(figsize=(8, 5))
plt.scatter(df['numeric_column1'], df['numeric_column2'], alpha=0.5)
plt.xlabel('Columna 1')
plt.ylabel('Columna 2')
plt.title('Scatter Plot con Matplotlib')
plt.show()

# Gráficos de Barras
fig = px.bar(df, x='category_column', y='numeric_column', color='category_column', title='Gráfico de Barras con Plotly')
fig.show()

plt.figure(figsize=(8, 5))
df.groupby('category_column')['numeric_column'].sum().plot(kind='bar', color='skyblue', edgecolor='black')
plt.xlabel('Categoría')
plt.ylabel('Valor')
plt.title('Gráfico de Barras con Matplotlib')
plt.show()
