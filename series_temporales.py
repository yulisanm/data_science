import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Cargar datos
df = pd.read_csv('time_series.csv', parse_dates=['date'], index_col='date')

# Visualizar la serie temporal
plt.figure(figsize=(10,5))
plt.plot(df, label='Serie Temporal')
plt.title('Visualización de la Serie Temporal')
plt.legend()
plt.show()

# Descomposición de la serie temporal
decomposition = seasonal_decompose(df, model='additive')
decomposition.plot()
plt.show()

# Ajustar modelo ARIMA
arima_model = ARIMA(df, order=(2,1,2))
arima_result = arima_model.fit()
print(arima_result.summary())

# Predicción con ARIMA
arima_forecast = arima_result.forecast(steps=10)
plt.figure(figsize=(10,5))
plt.plot(df, label='Serie Original')
plt.plot(arima_forecast, label='Pronóstico ARIMA', color='red')
plt.legend()
plt.show()

# Ajustar modelo SARIMAX
sarimax_model = SARIMAX(df, order=(2,1,2), seasonal_order=(1,1,1,12))
sarimax_result = sarimax_model.fit()
print(sarimax_result.summary())

# Predicción con SARIMAX
sarimax_forecast = sarimax_result.forecast(steps=10)
plt.figure(figsize=(10,5))
plt.plot(df, label='Serie Original')
plt.plot(sarimax_forecast, label='Pronóstico SARIMAX', color='green')
plt.legend()
plt.show()
