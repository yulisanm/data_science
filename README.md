# Estrategia Copilot

Este repositorio contiene una aplicación desarrollada para evaluar y visualizar los resultados de capacitaciones sobre GitHub Copilot. A continuación, se describe cada uno de los archivos presentes en el repositorio y cómo ejecutar la aplicación.

## Archivos en el Repositorio

- `00_Resumen.py`: Script principal de Streamlit que presenta un resumen de los resultados de las capacitaciones de GitHub Copilot.
- `auth_file_cuestionario.json`: Archivo de configuración que contiene las credenciales para autenticarse con la API de Google Sheets.
- `detalles_cuestionario.json`: Archivo JSON que contiene las preguntas del cuestionario y sus respuestas correctas.
- `pages/`: Carpeta que contiene scripts de Streamlit para diferentes secciones de la aplicación:
  - `01_Temáticas_Evaluadas.py`: Visualiza los resultados de las temáticas evaluadas.
  - `02_Preguntas_Selección_Múltiple.py`: Muestra los resultados de las preguntas de selección múltiple.
  - `03_Preguntas_Abiertas.py`: Genera nubes de palabras para las respuestas a preguntas abiertas.
  - `04_Asistencia_y_Cuestionario.py`: Visualiza la asistencia a las capacitaciones y las respuestas al cuestionario.
- `utils.py`: Script que contiene funciones de utilidad para cargar datos y generar visualizaciones.
- `requirements.txt`: Archivo que lista las dependencias de Python necesarias para ejecutar la aplicación.

## Cómo Ejecutar la Aplicación

Para ejecutar esta aplicación, necesitarás tener Python instalado en tu sistema. Sigue estos pasos para poner en marcha la aplicación:

1. Clona este repositorio en tu máquina local.
2. Abre una terminal y navega hasta el directorio del repositorio clonado.
3. Instala las dependencias necesarias ejecutando el comando: `pip install -r requirements.txt`
4. Inicia la aplicación de Streamlit ejecutando: `streamlit run 00_Resumen.py`
5. La aplicación debería abrirse automáticamente en tu navegador.

## Notas Adicionales

- Asegúrate de tener las credenciales correctas en `auth_file_cuestionario.json` para poder cargar los datos desde Google Sheets.